from sqlalchemy.orm import Session
from app.db.models.sub_drill import SubDrill
from app.schemas.sub_drill import SubDrillCreate, SubDrillUpdate
import uuid

class CRUDSubDrill:
    def get(self, db: Session, id: uuid.UUID):
        return db.query(SubDrill).filter(SubDrill.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(SubDrill).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: SubDrillCreate):
        db_obj = SubDrill(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: SubDrill, obj_in: SubDrillUpdate):
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: uuid.UUID):
        obj = db.query(SubDrill).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

crud_sub_drill = CRUDSubDrill()
