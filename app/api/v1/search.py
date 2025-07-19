from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.base import get_db
from app.db.models.drill import Drill
from app.db.models.drill_group import DrillGroup
from app.schemas.search import SearchResponse, SearchResult, ItemType

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search_drills_and_groups(
    *,
    db: AsyncSession = Depends(get_db),
    q: str = Query(..., description="Search query string", min_length=1),
    type_filter: Optional[ItemType] = Query(None, description="Filter by type (drill or drill_group)"),
    skip: int = Query(0, description="Skip first N results"),
    limit: int = Query(20, description="Limit number of results returned"),
) -> SearchResponse:
    """
    Search for drills and drill groups by name.
    Returns a combined list of results sorted by relevance.
    """
    search_term = f"%{q}%"
    results = []

    # Build the drill query if no type filter or if filtered for drills
    if type_filter is None or type_filter == ItemType.drill:
        drill_query = (
            select(Drill)
            .where(
                and_(
                    Drill.name.ilike(search_term),
                    or_(Drill.is_public == True, Drill.is_public == None)  # Include both public and unset drills
                )
            )
        )
        drill_results = await db.execute(drill_query)
        drills = drill_results.scalars().all()
        
        for drill in drills:
            results.append(
                SearchResult(
                    id=drill.id,
                    name=drill.name,
                    type=ItemType.drill,
                    description=drill.description,
                    drill_type=drill.drill_type
                )
            )

    # Build the drill group query if no type filter or if filtered for drill groups
    if type_filter is None or type_filter == ItemType.drill_group:
        drill_group_query = (
            select(DrillGroup)
            .where(
                and_(
                    DrillGroup.name.ilike(search_term),
                    or_(DrillGroup.is_public == True, DrillGroup.is_public == None)  # Include both public and unset groups
                )
            )
        )
        drill_group_results = await db.execute(drill_group_query)
        drill_groups = drill_group_results.scalars().all()
        
        for drill_group in drill_groups:
            results.append(
                SearchResult(
                    id=drill_group.id,
                    name=drill_group.name,
                    type=ItemType.drill_group,
                    description=drill_group.description,
                    tags=drill_group.tags,
                    difficulty=drill_group.difficulty
                )
            )

    # Sort results by name similarity to query (basic relevance sorting)
    results.sort(key=lambda x: (
        # Exact matches first
        x.name.lower() != q.lower(),
        # Then starts with query
        not x.name.lower().startswith(q.lower()),
        # Then by name length (shorter names first)
        len(x.name),
        # Finally alphabetically
        x.name.lower()
    ))

    # Apply pagination
    paginated_results = results[skip:skip + limit]

    return SearchResponse(
        total=len(results),
        items=paginated_results
    )
