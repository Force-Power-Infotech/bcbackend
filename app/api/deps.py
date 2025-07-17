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
    Get current user from session or Authorization header
    """
    # First try session
    username = request.session.get("username")
    if username:
        user = await crud_user.get_by_username(db, username=username)
        if user:
            return user

    # Then try Authorization header
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        token = auth[7:]  # Remove "Bearer " prefix
        try:
            from app.core.security import verify_token
            payload = verify_token(token)
            username = payload.get("sub")
            if username:
                user = await crud_user.get_by_username(db, username=username)
                if user:
                    return user
        except Exception:
            pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

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

async def get_optional_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current user from session if available, otherwise return None
    """
    username = request.session.get("username")
    if not username:
        return None
    
    user = await crud_user.get_by_username(db, username=username)
    return user

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
