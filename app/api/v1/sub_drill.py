from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.sub_drill import SubDrill, SubDrillCreate, SubDrillUpdate
from app.crud.crud_sub_drill import crud_sub_drill
from app.dependencies import get_db
import uuid

router = APIRouter(prefix="/sub-drills", tags=["SubDrills"])

@router.get("/", response_model=List[SubDrill])
def read_sub_drills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_sub_drill.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=SubDrill)
def create_sub_drill(obj_in: SubDrillCreate, db: Session = Depends(get_db)):
    return crud_sub_drill.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=SubDrill)
def read_sub_drill(id: uuid.UUID, db: Session = Depends(get_db)):
    db_obj = crud_sub_drill.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="SubDrill not found")
    return db_obj

@router.put("/{id}", response_model=SubDrill)
def update_sub_drill(id: uuid.UUID, obj_in: SubDrillUpdate, db: Session = Depends(get_db)):
    db_obj = crud_sub_drill.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="SubDrill not found")
    return crud_sub_drill.update(db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/{id}", response_model=SubDrill)
def delete_sub_drill(id: uuid.UUID, db: Session = Depends(get_db)):
    db_obj = crud_sub_drill.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="SubDrill not found")
    return crud_sub_drill.remove(db, id=id)
