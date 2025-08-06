from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class MetaDrillGroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class MetaDrillGroupCreate(MetaDrillGroupBase):
    pass

class MetaDrillGroupUpdate(MetaDrillGroupBase):
    pass

class MetaDrillGroupInDBBase(MetaDrillGroupBase):
    id: UUID
    created_at: datetime
    class Config:
        orm_mode = True

class MetaDrillGroup(MetaDrillGroupInDBBase):
    pass
