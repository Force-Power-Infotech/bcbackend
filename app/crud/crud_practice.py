from typing import Any, Dict, Optional, Union, List
from datetime import datetime

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.session import Session
from app.db.models.shot import Shot
from app.db.models.drill import Drill
from app.schemas.session import SessionCreate, SessionUpdate


async def get(db: AsyncSession, session_id: int) -> Optional[Session]:
    result = await db.execute(
        select(Session).where(Session.id == session_id)
    )
    return result.scalars().first()


async def get_with_related(db: AsyncSession, session_id: int) -> Optional[Session]:
    result = await db.execute(
        select(Session)
        .options(selectinload(Session.shots), selectinload(Session.drills))
        .where(Session.id == session_id)
    )
    return result.scalars().first()


async def get_by_user(
    db: AsyncSession, user_id: int, *, skip: int = 0, limit: int = 100
) -> List[Session]:
    result = await db.execute(
        select(Session)
        .where(Session.user_id == user_id)
        .order_by(Session.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create(db: AsyncSession, *, obj_in: SessionCreate, user_id: int) -> Session:
    db_obj = Session(
        user_id=user_id,
        title=obj_in.title,
        description=obj_in.description,
        duration_minutes=obj_in.duration_minutes,
        location=obj_in.location,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(
    db: AsyncSession, *, db_obj: Session, obj_in: Union[SessionUpdate, Dict[str, Any]]
) -> Session:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    stmt = (
        update(Session)
        .where(Session.id == db_obj.id)
        .values(**update_data)
        .returning(Session)
    )
    
    result = await db.execute(stmt)
    await db.commit()
    
    return result.scalars().first()


async def delete_session(db: AsyncSession, *, session_id: int) -> Optional[Session]:
    session = await get(db, session_id)
    if session:
        stmt = delete(Session).where(Session.id == session_id).returning(Session)
        result = await db.execute(stmt)
        await db.commit()
        return result.scalars().first()
    return None


async def get_session_stats(db: AsyncSession, session_id: int) -> Dict:
    # Get shot count and average accuracy
    shot_stats = await db.execute(
        select(
            func.count(Shot.id).label("shot_count"),
            func.avg(Shot.accuracy_score).label("avg_accuracy")
        )
        .where(Shot.session_id == session_id)
    )
    shot_result = shot_stats.first()
    
    # Get drill count
    drill_count = await db.execute(
        select(func.count(Drill.id))
        .where(Drill.session_id == session_id)
    )
    
    return {
        "shot_count": shot_result.shot_count if shot_result else 0,
        "average_accuracy": float(shot_result.avg_accuracy) if shot_result and shot_result.avg_accuracy else 0.0,
        "drill_count": drill_count.scalar() or 0
    }
