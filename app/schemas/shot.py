from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ShotTypeEnum(str, Enum):
    DRAW = "draw"
    DRIVE = "drive"
    WEIGHTED = "weighted"


class ShotBase(BaseModel):
    shot_type: ShotTypeEnum
    distance_meters: Optional[float] = None
    accuracy_score: int = Field(..., ge=1, le=10)
    notes: Optional[str] = None


class ShotCreate(ShotBase):
    session_id: int
    drill_id: Optional[int] = None


class ShotUpdate(ShotBase):
    shot_type: Optional[ShotTypeEnum] = None
    accuracy_score: Optional[int] = Field(None, ge=1, le=10)


class ShotInDBBase(ShotBase):
    id: int
    session_id: int
    drill_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Shot(ShotInDBBase):
    pass
