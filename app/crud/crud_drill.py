from typing import Any, Dict, Optional, Union, List
from datetime import datetime

from sqlalchemy import select, update, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.drill import Drill
from app.schemas.drill import DrillCreate, DrillUpdate


async def get(db: AsyncSession, drill_id: int) -> Optional[Drill]:
    """Get a drill by ID"""
    result = await db.execute(
        select(Drill).where(Drill.id == drill_id)
    )
    return result.scalars().first()


async def get_multi(
    db: AsyncSession, 
    *, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    difficulty: Optional[int] = None
) -> List[Drill]:
    """Get multiple drills with optional filtering"""
    query = select(Drill)
    
    # Apply search filter
    if search:
        query = query.filter(
            Drill.name.ilike(f"%{search}%") | 
            Drill.description.ilike(f"%{search}%")
        )
    
    # Apply difficulty filter
    if difficulty:
        query = query.filter(Drill.difficulty == difficulty)
    
    # Apply pagination
    query = query.offset(skip).limit(limit).order_by(Drill.created_at.desc())
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_count(
    db: AsyncSession,
    search: Optional[str] = None,
    difficulty: Optional[int] = None
) -> int:
    """Count drills with optional filtering"""
    query = select(func.count()).select_from(Drill)
    
    # Apply search filter
    if search:
        query = query.filter(
            Drill.name.ilike(f"%{search}%") | 
            Drill.description.ilike(f"%{search}%")
        )
    
    # Apply difficulty filter
    if difficulty:
        query = query.filter(Drill.difficulty == difficulty)
    
    result = await db.execute(query)
    return result.scalar() or 0


async def create(db: AsyncSession, *, obj_in: DrillCreate) -> Drill:
    """Create a new drill"""
    db_obj = Drill(
        session_id=obj_in.session_id,
        name=obj_in.name,
        description=obj_in.description,
        target_score=obj_in.target_score,
        difficulty=obj_in.difficulty,
        drill_type=obj_in.drill_type,
        duration_minutes=obj_in.duration_minutes
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(db: AsyncSession, *, db_obj: Drill, obj_in: Union[DrillUpdate, Dict[str, Any]]) -> Drill:
    """Update a drill"""
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def remove(db: AsyncSession, *, drill_id: int) -> Drill:
    """Delete a drill"""
    result = await db.execute(select(Drill).where(Drill.id == drill_id))
    obj = result.scalars().first()
    if obj:
        await db.delete(obj)
        await db.commit()
    return obj


async def get_template_drills(
    db: AsyncSession,
    *,
    drill_type: Optional[str] = None,  
    difficulty_min: Optional[int] = None,
    difficulty_max: Optional[int] = None,
    limit: int = 10
) -> List[Drill]:
    """
    Get template drills (special drills not attached to specific sessions)
    that can be used as templates for creating new session drills
    """
    # In a real implementation, you'd have a column like is_template to identify template drills
    # For now, we'll simulate this by selecting drills from a specific template session ID
    template_session_id = 0  # Special ID for template drills
    
    query = select(Drill).where(Drill.session_id == template_session_id)
    
    # Apply type filter if provided
    if drill_type:
        query = query.filter(Drill.name.ilike(f"%{drill_type}%"))
    
    # Apply difficulty range if provided
    if difficulty_min is not None:
        query = query.filter(Drill.difficulty >= difficulty_min)
    if difficulty_max is not None:
        query = query.filter(Drill.difficulty <= difficulty_max)
    
    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
