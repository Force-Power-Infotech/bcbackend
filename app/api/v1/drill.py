from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.user import User
from app.schemas.drill import Drill, DrillCreate, DrillUpdate
from app.api import deps
from app.crud import crud_drill

router = APIRouter()

@router.get("/", response_model=List[Drill])
async def get_drills(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    difficulty: Optional[int] = None,
) -> Any:
    """
    Get all drills with optional filtering.
    """
    drills = await crud_drill.get_multi(
        db, skip=skip, limit=limit, search=search, difficulty=difficulty
    )
    return drills

@router.post("/", response_model=Drill)
async def create_drill(
    *,
    db: AsyncSession = Depends(get_db),
    drill_in: DrillCreate,
) -> Any:
    """
    Create a new drill. Session ID is optional to allow template drills.
    """
    try:
        drill = await crud_drill.create(db, obj_in=drill_in)
        return drill
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Could not create drill: {str(e)}"
        )

@router.get("/{drill_id}", response_model=Drill)
async def get_drill(
    drill_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific drill by ID.
    """
    drill = await crud_drill.get(db, drill_id=drill_id)
    if not drill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill not found",
        )
    return drill

@router.put("/{drill_id}", response_model=Drill)
async def update_drill(
    *,
    db: AsyncSession = Depends(get_db),
    drill_id: int,
    drill_in: DrillUpdate,
) -> Any:
    """
    Update a drill.
    """
    drill = await crud_drill.get(db, drill_id=drill_id)
    if not drill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill not found",
        )
    drill = await crud_drill.update(db, db_obj=drill, obj_in=drill_in)
    return drill

@router.delete("/{drill_id}", response_model=Drill)
async def delete_drill(
    *,
    db: AsyncSession = Depends(get_db),
    drill_id: int,
) -> Any:
    """
    Delete a drill.
    """
    drill = await crud_drill.get(db, drill_id=drill_id)
    if not drill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill not found",
        )
    drill = await crud_drill.remove(db, drill_id=drill_id)
    return drill
