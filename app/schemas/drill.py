from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DrillBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_score: int = Field(default=80, ge=0, le=100, description="Target score (0-100)")
    difficulty: int = Field(default=1, ge=1, le=5, description="Difficulty level (1-5)")
    drill_type: str = Field(description="Type of drill (DRAW, DRIVE, etc.)")
    duration_minutes: int = Field(default=30, ge=5, le=120, description="Duration in minutes")


class DrillCreate(DrillBase):
    session_id: Optional[int] = None
    description: str  # Make description required for create


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
