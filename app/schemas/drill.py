from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DrillBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_score: Optional[int] = Field(None, ge=1, le=10)
    difficulty: Optional[int] = Field(None, ge=1, le=10)
    drill_type: Optional[str] = Field(None, description="Type of drill (DRAW, DRIVE, etc.)")
    duration_minutes: Optional[int] = Field(None, ge=1, description="Duration in minutes")


class DrillCreate(DrillBase):
    session_id: Optional[int] = None
    name: str
    description: str
    drill_type: str
    duration_minutes: int


class DrillUpdate(DrillBase):
    name: Optional[str] = None


class DrillInDBBase(DrillBase):
    id: int
    session_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Drill(DrillInDBBase):
    pass


# Schema for Drill with stats
class DrillWithStats(Drill):
    shot_count: int = 0
    average_accuracy: float = 0.0
    completion_rate: float = 0.0  # Percentage of shots that met target score
