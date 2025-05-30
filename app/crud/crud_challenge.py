from typing import Any, Dict, Optional, Union, List
from datetime import datetime, timedelta

from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.challenge import Challenge, ChallengeStatus
from app.db.models.user import User
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate


async def get(db: AsyncSession, challenge_id: int) -> Optional[Challenge]:
    result = await db.execute(
        select(Challenge).where(Challenge.id == challenge_id)
    )
    return result.scalars().first()


async def get_with_users(db: AsyncSession, challenge_id: int) -> Optional[Dict]:
    result = await db.execute(
        select(Challenge, User.username.label("sender_username"), User.username.label("recipient_username"))
        .join(User, Challenge.sender_id == User.id, isouter=True)
        .join(User, Challenge.recipient_id == User.id, isouter=True)
        .where(Challenge.id == challenge_id)
    )
    row = result.first()
    if not row:
        return None
    
    challenge, sender_username, recipient_username = row
    return {
        **challenge.__dict__,
        "sender_username": sender_username,
        "recipient_username": recipient_username
    }


async def get_user_challenges(
    db: AsyncSession, 
    user_id: int, 
    *, 
    status: Optional[List[ChallengeStatus]] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[Challenge]:
    query = (
        select(Challenge)
        .where(
            or_(
                Challenge.sender_id == user_id,
                Challenge.recipient_id == user_id
            )
        )
    )
    
    if status:
        query = query.where(Challenge.status.in_(status))
    
    result = await db.execute(
        query
        .order_by(Challenge.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    
    return result.scalars().all()


async def create(db: AsyncSession, *, obj_in: ChallengeCreate, sender_id: int) -> Challenge:
    # Set expiration date (default 7 days)
    expires_at = datetime.utcnow() + timedelta(days=7)
    
    db_obj = Challenge(
        sender_id=sender_id,
        recipient_id=obj_in.recipient_id,
        title=obj_in.title,
        description=obj_in.description,
        drill_type=obj_in.drill_type,
        target_score=obj_in.target_score,
        status=ChallengeStatus.PENDING,
        expires_at=expires_at
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(
    db: AsyncSession, *, db_obj: Challenge, obj_in: Union[ChallengeUpdate, Dict[str, Any]]
) -> Challenge:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    stmt = (
        update(Challenge)
        .where(Challenge.id == db_obj.id)
        .values(**update_data)
        .returning(Challenge)
    )
    
    result = await db.execute(stmt)
    await db.commit()
    
    return result.scalars().first()


async def update_status(
    db: AsyncSession, challenge_id: int, status: ChallengeStatus
) -> Optional[Challenge]:
    stmt = (
        update(Challenge)
        .where(Challenge.id == challenge_id)
        .values(status=status)
        .returning(Challenge)
    )
    
    result = await db.execute(stmt)
    await db.commit()
    
    return result.scalars().first()


async def delete_challenge(db: AsyncSession, *, challenge_id: int) -> Optional[Challenge]:
    challenge = await get(db, challenge_id)
    if challenge:
        stmt = delete(Challenge).where(Challenge.id == challenge_id).returning(Challenge)
        result = await db.execute(stmt)
        await db.commit()
        return result.scalars().first()
    return None
