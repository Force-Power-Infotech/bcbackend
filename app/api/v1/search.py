from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.base import get_db
from app.db.models.drill import Drill
from app.db.models.drill_group import DrillGroup

# Create router instance
router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=SearchResponse)
async def search(
    query: str,
    db: AsyncSession = Depends(get_db)
) -> SearchResponse:
    """
    Search for drills and drill groups.
    Returns matches from both drills and drill groups sorted by relevance.
    """
    search_term = f"%{query}%"
    search_exact = query.lower()
    search_starts = f"{query}%"
    
    # Search drills
    drill_query = select(Drill).where(
        or_(
            Drill.name.ilike(search_exact),  # Exact match
            Drill.name.ilike(search_starts),  # Starts with
            Drill.name.ilike(search_term),    # Contains
            Drill.description.ilike(search_term)  # Description contains
        )
    )
    drill_results = await db.execute(drill_query)
    drills = drill_results.scalars().all()

    # Search public drill groups
    drill_group_query = select(DrillGroup).where(
        and_(
            or_(
                DrillGroup.name.ilike(search_exact),  # Exact match
                DrillGroup.name.ilike(search_starts),  # Starts with
                DrillGroup.name.ilike(search_term),    # Contains
                DrillGroup.description.ilike(search_term)  # Description contains
            ),
            DrillGroup.is_public.is_(True)  # Only public drill groups
        )
    )
    drill_group_results = await db.execute(drill_group_query)
    drill_groups = drill_group_results.scalars().all()

    # Combine results
    results = []
    
    # Helper function to get relevance score
    def get_relevance_score(name: str) -> int:
        name_lower = name.lower()
        if name_lower == search_exact:  # Exact match
            return 0
        if name_lower.startswith(query.lower()):  # Starts with
            return 1
        if query.lower() in name_lower:  # Contains
            return 2
        return 3  # Description match
    
    # Add drills
    for drill in drills:
        results.append(
            SearchResult(
                id=drill.id,
                name=drill.name,
                type="drill",
                description=drill.description
            )
        )

    # Add drill groups
    for group in drill_groups:
        results.append(
            SearchResult(
                id=group.id,
                name=group.name,
                type="drill_group",
                description=group.description
            )
        )

    # Sort results by relevance score and then alphabetically
    results.sort(key=lambda x: (get_relevance_score(x.name), x.name.lower()))

    return SearchResponse(
        items=results,
        total=len(results)
    )
