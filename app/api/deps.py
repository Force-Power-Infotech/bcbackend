from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.schemas.user import User
from app.crud import crud_user

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current user from session
    """
    username = request.session.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user = await crud_user.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

async def get_current_user_optional(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Similar to get_current_user but doesn't raise an exception if session is missing
    Returns None if no session or invalid session is provided
    """
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Check if the user is active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user

def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Check if the user is an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user
