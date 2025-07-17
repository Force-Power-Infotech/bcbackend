from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.user import User
from app.schemas.drill_group import DrillGroup, DrillGroupCreate, DrillGroupUpdate, DrillGroupInDBBase
from app.api import deps
from app.crud import crud_drill_group, crud_drill

router = APIRouter()


@router.get("/", response_model=List[DrillGroup])
async def get_drill_groups(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, description="Skip first N drill groups"),
    limit: int = Query(100, description="Limit number of drill groups returned"),
) -> Any:
    """Get all drill groups."""
    drill_groups = await crud_drill_group.get_multi(
        db, skip=skip, limit=limit
    )
    return drill_groups


@router.post("/", response_model=DrillGroupInDBBase)
async def create_drill_group(
    *,
    db: AsyncSession = Depends(get_db),
    drill_group_in: DrillGroupCreate,
    current_user: Optional[User] = Depends(deps.get_current_user_optional),
) -> Any:
    """
    Create a new drill group.
    
    - name: Name of the drill group
    - description: Optional description
    - drill_ids: Optional list of drill IDs to add to the group
    - is_public: Whether the group is publicly visible (default: true)
    - tags: Optional list of tags for categorization
    - difficulty: Optional difficulty level (1-5)
    """
    # No user ID required
    user_id = None
    
    # Create the drill group with the user ID (which may be None)
    try:
        drill_group = await crud_drill_group.create(
            db=db, 
            obj_in=drill_group_in,
            user_id=user_id
        )
        # Return a serializable response
        return {
            "id": drill_group.id,
            "user_id": drill_group.user_id,
            "name": drill_group.name,
            "description": drill_group.description,
            "is_public": getattr(drill_group, "is_public", True),
            "difficulty": getattr(drill_group, "difficulty", 1),
            "tags": getattr(drill_group, "tags", []),
            "created_at": drill_group.created_at,
            "updated_at": drill_group.updated_at
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Could not create drill group: {str(e)}"
        )


@router.get("/{drill_group_id}", response_model=DrillGroup)
async def get_drill_group(
    *,
    db: AsyncSession = Depends(get_db),
    drill_group_id: int = Path(..., description="ID of the drill group to get"),
) -> Any:
    """Get a specific drill group by ID."""
    drill_group = await crud_drill_group.get(db, drill_group_id=drill_group_id)
    if not drill_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill group not found"
        )
    return drill_group


@router.put("/{drill_group_id}", response_model=DrillGroup)
async def update_drill_group(
    *,
    db: AsyncSession = Depends(get_db),
    drill_group_id: int = Path(..., description="ID of the drill group to update"),
    drill_group_in: DrillGroupUpdate,
    current_user: Optional[User] = Depends(deps.get_current_user_optional),
) -> Any:
    """Update a drill group."""
    drill_group = await crud_drill_group.get(db, drill_group_id=drill_group_id)
    if not drill_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill group not found"
        )
    
    # No authorization check - anyone can update a drill group
    
    drill_group = await crud_drill_group.update(
        db=db, db_obj=drill_group, obj_in=drill_group_in
    )
    return drill_group


@router.delete("/{drill_group_id}", response_model=DrillGroup)
async def delete_drill_group(
    *,
    db: AsyncSession = Depends(get_db),
    drill_group_id: int = Path(..., description="ID of the drill group to delete"),
    current_user: Optional[User] = Depends(deps.get_current_user_optional),
) -> Any:
    """Delete a drill group."""
    drill_group = await crud_drill_group.get(db, drill_group_id=drill_group_id)
    if not drill_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill group not found"
        )
    
    # No authorization check - anyone can delete a drill group
    
    drill_group = await crud_drill_group.remove(db=db, drill_group_id=drill_group_id)
    return drill_group


@router.post("/{drill_group_id}/drills/{drill_id}")
async def add_drill_to_group(
    *,
    db: AsyncSession = Depends(get_db),
    drill_group_id: int = Path(..., description="ID of the drill group"),
    drill_id: int = Path(..., description="ID of the drill to add"),
) -> Any:
    """Add a drill to a drill group."""
    drill_group = await crud_drill_group.get(db, drill_group_id=drill_group_id)
    if not drill_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill group not found"
        )
    
    drill = await crud_drill.get(db, drill_id=drill_id)
    if not drill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill not found"
        )
    
    await crud_drill_group.add_drill_to_group(
        db=db, drill_group_id=drill_group_id, drill_id=drill_id
    )
    return {"message": "Drill added to group successfully"}


@router.delete("/{drill_group_id}/drills/{drill_id}")
async def remove_drill_from_group(
    *,
    db: AsyncSession = Depends(get_db),
    drill_group_id: int = Path(..., description="ID of the drill group"),
    drill_id: int = Path(..., description="ID of the drill to remove"),
) -> Any:
    """Remove a drill from a drill group."""
    drill_group = await crud_drill_group.get(db, drill_group_id=drill_group_id)
    if not drill_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill group not found"
        )
    if drill_group.user_id is not None and (current_user is None or drill_group.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this drill group"
        )
    
    await crud_drill_group.remove_drill_from_group(
        db=db, drill_group_id=drill_group_id, drill_id=drill_id
    )
    return {"message": "Drill removed from group successfully"}


@router.put("/{drill_group_id}/drills", response_model=DrillGroup)
async def update_drill_group_drills(
    *,
    db: AsyncSession = Depends(get_db),
    drill_group_id: int = Path(..., description="ID of the drill group to update"),
    drill_ids: List[int] = Query(..., description="List of drill IDs to set for the group"),
    current_user: Optional[User] = Depends(deps.get_current_user_optional),
) -> Any:
    """Update the drills in a drill group."""
    drill_group = await crud_drill_group.get(db, drill_group_id=drill_group_id)
    if not drill_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill group not found"
        )
    
    # No authorization check - anyone can modify drill groups
    
    # Verify all drills exist
    drills = []
    for drill_id in drill_ids:
        drill = await crud_drill.get(db, drill_id=drill_id)
        if not drill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Drill with id {drill_id} not found"
            )
        drills.append(drill)
    
    # Update the drills
    drill_group.drills = drills
    await db.commit()
    await db.refresh(drill_group)
    return drill_group
