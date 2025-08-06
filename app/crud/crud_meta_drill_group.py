from sqlalchemy.orm import Session
from app.db.models.meta_drill_group import MetaDrillGroup
from app.schemas.meta_drill_group import MetaDrillGroupCreate, MetaDrillGroupUpdate
import uuid

class CRUDMetaDrillGroup:
    def get(self, db: Session, id: uuid.UUID):
        return db.query(MetaDrillGroup).filter(MetaDrillGroup.id == id).first()

    async def get_multi(self, db, skip: int = 0, limit: int = 100):
        from sqlalchemy import select
        result = await db.execute(
            select(MetaDrillGroup).offset(skip).limit(limit)
        )
        return result.scalars().all()

    def create(self, db: Session, obj_in: MetaDrillGroupCreate):
        db_obj = MetaDrillGroup(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: MetaDrillGroup, obj_in: MetaDrillGroupUpdate):
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: uuid.UUID):
        obj = db.query(MetaDrillGroup).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

crud_meta_drill_group = CRUDMetaDrillGroup()
