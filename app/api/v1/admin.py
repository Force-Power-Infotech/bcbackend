from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.user import User
from app.api import deps
from app.crud import crud_user

router = APIRouter()


@router.get("/users", response_model=List[User])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),  # Admin only
) -> Any:
    """
    Get all users (admin only).
    """
    users = await crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.put("/users/{user_id}/make-admin", response_model=User)
async def make_user_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),  # Admin only
) -> Any:
    """
    Make a user an admin (admin only).
    """
    user = await crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Update to admin
    updated_user = await crud_user.update(db, db_obj=user, obj_in={"is_admin": True})
    return updated_user


@router.put("/users/{user_id}/deactivate", response_model=User)
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),  # Admin only
) -> Any:
    """
    Deactivate a user (admin only).
    """
    user = await crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Don't allow deactivating yourself
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate yourself",
        )
    
    # Deactivate user
    updated_user = await crud_user.update(db, db_obj=user, obj_in={"is_active": False})
    return updated_user
