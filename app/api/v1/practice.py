from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.user import User
from app.schemas.session import Session, SessionCreate, SessionUpdate, SessionWithStats
from app.schemas.shot import Shot, ShotCreate
from app.schemas.drill import Drill, DrillCreate
from app.api import deps
from app.crud import crud_practice

router = APIRouter()


@router.post("/sessions", response_model=Session)
async def create_session(
    session_in: SessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new practice session.
    """
    session = await crud_practice.create(db, obj_in=session_in, user_id=current_user.id)
    return session


@router.get("/sessions", response_model=List[Session])
async def read_sessions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all practice sessions for current user.
    """
    sessions = await crud_practice.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return sessions


@router.get("/sessions/{session_id}", response_model=SessionWithStats)
async def read_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific practice session by ID.
    """
    session = await crud_practice.get(db, session_id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    
    # Check if the session belongs to the current user
    if session.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Get session statistics
    stats = await crud_practice.get_session_stats(db, session_id)
    
    # Combine the session data with stats
    session_data = {
        **session.__dict__,
        "shot_count": stats["shot_count"],
        "average_accuracy": stats["average_accuracy"],
        "drill_count": stats["drill_count"],
    }
    
    return session_data


@router.put("/sessions/{session_id}", response_model=Session)
async def update_session(
    session_id: int,
    session_in: SessionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a practice session.
    """
    session = await crud_practice.get(db, session_id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    
    # Check if the session belongs to the current user
    if session.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    session = await crud_practice.update(db, db_obj=session, obj_in=session_in)
    return session


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> None:
    """
    Delete a practice session.
    """
    session = await crud_practice.get(db, session_id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    
    # Check if the session belongs to the current user
    if session.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    await crud_practice.delete_session(db, session_id=session_id)
