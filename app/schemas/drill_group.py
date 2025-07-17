from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from .drill import Drill


class DrillGroupBase(BaseModel):
    name: str = Field(..., description="Name of the drill group")
    description: Optional[str] = Field(None, description="Description of the drill group")
    image: Optional[str] = Field(None, description="URL of the drill group image")


class DrillGroupCreate(DrillGroupBase):
    drill_ids: Optional[List[int]] = Field(default=[], description="List of drill IDs to add to the group")
    is_public: bool = Field(default=True, description="Whether the drill group is public")
    tags: Optional[List[str]] = Field(default=[], description="Tags for categorizing the drill group")
    difficulty: Optional[int] = Field(default=1, ge=1, le=5, description="Difficulty level of the drill group")


class DrillGroupUpdate(DrillGroupBase):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None


class DrillGroupInDBBase(DrillGroupBase):
    id: int
    user_id: Optional[int] = Field(default=1)  # Default to user ID 1
    is_public: bool = Field(default=True)
    difficulty: Optional[int] = Field(default=1)
    tags: Optional[List[str]] = Field(default=[])
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DrillGroup(DrillGroupInDBBase):
    drills: Optional[List[Drill]] = Field(default=[])
