from typing import Any, Dict, Optional, Union, List

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get a user by email."""
    query = select(User).where(User.email == email)
    async with db.begin():
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()


async def get_by_phone(db: AsyncSession, phone_number: str) -> Optional[User]:
    """Get a user by phone number."""
    query = select(User).where(User.phone_number == phone_number)
    async with db.begin():
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()


async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Get a user by username."""
    query = select(User).where(User.username == username)
    async with db.begin():
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()


async def get(db: AsyncSession, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    query = select(User).where(User.id == user_id)
    async with db.begin():
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()


async def create(db: AsyncSession, *, obj_in: UserCreate) -> User:
    """Create a new user."""
    db_obj = User(
        email=obj_in.email,
        username=obj_in.username,
        hashed_password=get_password_hash(obj_in.password),
        phone_number=obj_in.phone_number,
        full_name=obj_in.full_name,
        is_active=True,
        is_admin=False
    )
    async with db.begin():
        db.add(db_obj)
    await db.refresh(db_obj)
    return db_obj


async def update(
    db: AsyncSession,
    *,
    db_obj: User,
    obj_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    """Update a user."""
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def authenticate(
    db: AsyncSession, *, username: str, password: str
) -> Optional[User]:
    """Authenticate a user."""
    user = await get_by_username(db, username=username)
    if not user:
        user = await get_by_email(db, email=username)
        if not user:
            return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def is_active(user: User) -> bool:
    """Check if user is active."""
    return user.is_active


async def is_admin(user: User) -> bool:
    """Check if user is admin."""
    return user.is_admin


async def mark_phone_verified(
    db: AsyncSession, *, user: User
) -> User:
    """Mark user's phone as verified."""
    user.phone_verified = True
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def mark_email_verified(
    db: AsyncSession, *, user: User
) -> User:
    """Mark user's email as verified."""
    user.email_verified = True
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
