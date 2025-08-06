from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List
from app.schemas.meta_drill_group import MetaDrillGroup, MetaDrillGroupCreate, MetaDrillGroupUpdate
from app.crud.crud_meta_drill_group import crud_meta_drill_group
from app.dependencies import get_db
import uuid

router = APIRouter(prefix="/meta-drill-groups", tags=["MetaDrillGroups"])

@router.get("/", response_model=List[MetaDrillGroup])
async def read_meta_drill_groups(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud_meta_drill_group.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=MetaDrillGroup)
async def create_meta_drill_group(obj_in: MetaDrillGroupCreate, db: AsyncSession = Depends(get_db)):
    # You may need to update the CRUD method to be async if you want full async support
    return await crud_meta_drill_group.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=MetaDrillGroup)
async def read_meta_drill_group(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    db_obj = await crud_meta_drill_group.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="MetaDrillGroup not found")
    return db_obj

@router.put("/{id}", response_model=MetaDrillGroup)
async def update_meta_drill_group(id: uuid.UUID, obj_in: MetaDrillGroupUpdate, db: AsyncSession = Depends(get_db)):
    db_obj = await crud_meta_drill_group.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="MetaDrillGroup not found")
    return await crud_meta_drill_group.update(db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/{id}", response_model=MetaDrillGroup)
async def delete_meta_drill_group(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    db_obj = await crud_meta_drill_group.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="MetaDrillGroup not found")
    return await crud_meta_drill_group.remove(db, id=id)
