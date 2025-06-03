from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from .drill import Drill


class DrillGroupBase(BaseModel):
    name: str = Field(..., description="Name of the drill group")
    description: Optional[str] = Field(None, description="Description of the drill group")


class DrillGroupCreate(DrillGroupBase):
    pass


class DrillGroupUpdate(DrillGroupBase):
    name: Optional[str] = None
    description: Optional[str] = None


class DrillGroupInDBBase(DrillGroupBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DrillGroup(DrillGroupInDBBase):
    drills: List[Drill] = []
