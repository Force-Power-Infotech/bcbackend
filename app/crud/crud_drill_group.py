from typing import Any, Dict, Optional, Union, List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.drill_group import DrillGroup, DrillGroupDrills
from app.db.models.drill import Drill
from app.schemas.drill_group import DrillGroupCreate, DrillGroupUpdate


async def get(db: AsyncSession, drill_group_id: int) -> Optional[DrillGroup]:
    """Get a drill group by ID"""
    result = await db.execute(
        select(DrillGroup)
        .options(selectinload(DrillGroup.drills))
        .where(DrillGroup.id == drill_group_id)
    )
    return result.scalars().first()


async def get_multi(
    db: AsyncSession,
    *,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[DrillGroup]:
    """Get multiple drill groups, optionally filtered by user"""
    query = select(DrillGroup).options(selectinload(DrillGroup.drills))
    
    if user_id is not None:
        query = query.where(DrillGroup.user_id == user_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_drill_group_drills(
    db: AsyncSession,
    *,
    drill_group_id: int
) -> List[Drill]:
    """Get all drills in a drill group"""
    result = await db.execute(
        select(Drill)
        .join(DrillGroupDrills)
        .where(DrillGroupDrills.drill_group_id == drill_group_id)
    )
    return result.scalars().all()


async def create(
    db: AsyncSession,
    *,
    obj_in: DrillGroupCreate,
    user_id: Optional[int] = None
) -> DrillGroup:
    """Create a new drill group"""
    # Create the basic drill group
    db_obj = DrillGroup(
        user_id=user_id,
        name=obj_in.name,
        description=obj_in.description,
        # We could store these in JSON columns or separate tables
        is_public=getattr(obj_in, "is_public", True),
        difficulty=getattr(obj_in, "difficulty", 1),
        tags=getattr(obj_in, "tags", [])
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    # Add drills to the group if provided
    if hasattr(obj_in, "drill_ids") and obj_in.drill_ids:
        from app.crud import crud_drill
        valid_drills = []
        for drill_id in obj_in.drill_ids:
            try:
                drill = await crud_drill.get(db, drill_id=drill_id)
                if drill:
                    valid_drills.append(drill)
            except Exception:
                # Skip invalid drill IDs
                pass
        
        if valid_drills:
            db_obj.drills = valid_drills
            await db.commit()
        
    await db.refresh(db_obj)
    return db_obj


"""This function has been merged into the main 'create' function with an optional user_id parameter"""


async def update(
    db: AsyncSession,
    *,
    db_obj: DrillGroup,
    obj_in: Union[DrillGroupUpdate, Dict[str, Any]]
) -> DrillGroup:
    """Update a drill group"""
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def remove(db: AsyncSession, *, drill_group_id: int) -> DrillGroup:
    """Delete a drill group"""
    result = await db.execute(
        select(DrillGroup).where(DrillGroup.id == drill_group_id)
    )
    obj = result.scalars().first()
    if obj:
        await db.delete(obj)
        await db.commit()
    return obj


async def add_drill_to_group(
    db: AsyncSession,
    *,
    drill_group_id: int,
    drill_id: int
) -> DrillGroupDrills:
    """Add a drill to a drill group"""
    db_obj = DrillGroupDrills(
        drill_group_id=drill_group_id,
        drill_id=drill_id
    )
    db.add(db_obj)
    await db.commit()
    return db_obj


async def remove_drill_from_group(
    db: AsyncSession,
    *,
    drill_group_id: int,
    drill_id: int
) -> None:
    """Remove a drill from a drill group"""
    result = await db.execute(
        select(DrillGroupDrills).where(
            and_(
                DrillGroupDrills.drill_group_id == drill_group_id,
                DrillGroupDrills.drill_id == drill_id
            )
        )
    )
    obj = result.scalars().first()
    if obj:
        await db.delete(obj)
        await db.commit()


async def update_drills(
    db: AsyncSession,
    *,
    drill_group: DrillGroup,
    drill_ids: List[int]
) -> DrillGroup:
    """Update the drills in a drill group"""
    # Clear existing drills
    drill_group.drills = []
    await db.flush()
    
    # Add new drills
    result = await db.execute(
        select(Drill).where(Drill.id.in_(drill_ids))
    )
    drills = result.scalars().all()
    drill_group.drills = drills
    
    await db.commit()
    await db.refresh(drill_group)
    return drill_group


async def get_admin_user_id(db: AsyncSession) -> Optional[int]:
    """Get the admin user ID to use for drill groups, or None if no users exist"""
    from app.crud.crud_user import get_by_email
    from app.core.config import settings
    
    # Try to get the admin user
    try:
        admin_user = await get_by_email(db, email=settings.ADMIN_EMAIL)
        if admin_user:
            return admin_user.id
    except Exception:
        pass
    
    # If no admin user, get the first user
    from sqlalchemy import select
    from app.db.models.user import User
    
    result = await db.execute(select(User).limit(1))
    user = result.scalars().first()
    
    if user:
        return user.id
    
    # If no users exist, return None
    return None
