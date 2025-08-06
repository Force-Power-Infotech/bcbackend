from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class SubDrillBase(BaseModel):
    title: str
    instruction: Optional[str] = None
    drill_id: UUID

class SubDrillCreate(SubDrillBase):
    pass

class SubDrillUpdate(SubDrillBase):
    pass

class SubDrillInDBBase(SubDrillBase):
    id: UUID
    created_at: datetime
    class Config:
        orm_mode = True

class SubDrill(SubDrillInDBBase):
    pass
