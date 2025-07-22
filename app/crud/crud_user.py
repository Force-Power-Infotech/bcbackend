from typing import Any, Dict, Optional, Union
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.db.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate


async def get_by_email(db: AsyncSession, email: str) -> Optional[UserModel]:
    stmt = select(UserModel).where(UserModel.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_by_phone(db: AsyncSession, phone_number: str) -> Optional[UserModel]:
    stmt = select(UserModel).where(UserModel.phone_number == phone_number)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_by_username(db: AsyncSession, username: str) -> Optional[UserModel]:
    stmt = select(UserModel).where(UserModel.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get(db: AsyncSession, user_id: int) -> Optional[UserModel]:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create(db: AsyncSession, *, obj_in: UserCreate) -> UserModel:
    db_obj = UserModel(
        email=obj_in.email,
        username=obj_in.username,
        hashed_password=get_password_hash(obj_in.password),
        phone_number=obj_in.phone_number,
        full_name=obj_in.full_name,
        is_active=True,
        is_admin=False
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(
    db: AsyncSession,
    *,
    db_obj: UserModel,
    obj_in: Union[UserUpdate, Dict[str, Any]]
) -> UserModel:
    update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def authenticate(db: AsyncSession, *, username: str, password: str) -> Optional[UserModel]:
    user = await get_by_username(db, username=username)
    if not user:
        user = await get_by_email(db, email=username)
        if not user:
            return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def mark_phone_verified(db: AsyncSession, *, user: UserModel) -> UserModel:
    user.phone_verified = True
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def mark_email_verified(db: AsyncSession, *, user: UserModel) -> UserModel:
    user.email_verified = True
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_otp(db: AsyncSession, *, user: UserModel, otp: Optional[str] = None) -> UserModel:
    """
    Update the OTP for a user and save to database
    """
    user.otp = otp
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_count(
    db: AsyncSession, 
    created_at_before: Optional[datetime] = None,
    created_at_after: Optional[datetime] = None
) -> int:
    """
    Get the total count of users in the database, with optional date filters.
    
    Args:
        db: AsyncSession - The database session
        created_at_before: Optional[datetime] - Filter users created before this date
        created_at_after: Optional[datetime] - Filter users created after this date
        
    Returns:
        int: The total number of users
    """
    query = select(func.count()).select_from(UserModel)
    
    # Apply filters if provided
    if created_at_before:
        query = query.where(UserModel.created_at < created_at_before)
    if created_at_after:
        query = query.where(UserModel.created_at >= created_at_after)
    
    result = await db.execute(query)
    return result.scalar_one()


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[UserModel]:
    """
    Get all users with pagination support.
    
    Args:
        db: AsyncSession - The database session
        skip: int - Number of users to skip (for pagination)
        limit: int - Maximum number of users to return
        
    Returns:
        List[UserModel]: List of users
    """
    query = select(UserModel).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
