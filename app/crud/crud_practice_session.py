from typing import Dict, List, Optional, Any
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.models.practice_session import PracticeSession
from app.db.models.drill_group import DrillGroup
from app.db.models.drill import Drill
from app.db.models.user import User


async def create_practice_sessions(
    db: AsyncSession, 
    user_id: int,
    drill_group_id: UUID,
    drill_ids: List[UUID]
) -> List[PracticeSession]:
    """Create multiple practice session entries."""
    
    # Verify user exists
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    
    # Verify drill group exists
    drill_group = await db.execute(select(DrillGroup).where(DrillGroup.id == drill_group_id))
    drill_group = drill_group.scalars().first()
    if not drill_group:
        raise ValueError(f"DrillGroup with ID {drill_group_id} not found")
    
    # Verify all drills exist
    drills = await db.execute(select(Drill).where(Drill.id.in_(drill_ids)))
    found_drills = drills.scalars().all()
    found_drill_ids = {drill.id for drill in found_drills}
    missing_drill_ids = set(drill_ids) - found_drill_ids
    
    if missing_drill_ids:
        raise ValueError(f"Drills with IDs {missing_drill_ids} not found")
    
    # Create practice session entries
    practice_sessions = []
    for drill_id in drill_ids:
        # Create new practice session
        practice_session = PracticeSession(
            user_id=user_id,
            drill_group_id=drill_group_id,
            drill_id=drill_id
        )
        db.add(practice_session)
        practice_sessions.append(practice_session)
    
    await db.flush()  # This will populate the IDs
    return practice_sessions


async def get_user_practice_sessions(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[PracticeSession]:
    """Get all practice sessions for a user"""
    result = await db.execute(
        select(PracticeSession)
        .where(PracticeSession.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(PracticeSession.created_at.desc())
    )
    return result.scalars().all()


async def get_drill_group_practice_sessions(
    db: AsyncSession,
    drill_group_id: UUID,
    skip: int = 0,
    limit: int = 100
) -> List[PracticeSession]:
    """Get all practice sessions for a drill group"""
    result = await db.execute(
        select(PracticeSession)
        .where(PracticeSession.drill_group_id == drill_group_id)
        .offset(skip)
        .limit(limit)
        .order_by(PracticeSession.created_at.desc())
    )
    return result.scalars().all()
