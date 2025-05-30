from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DrillBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_score: Optional[int] = Field(None, ge=1, le=10)
    difficulty: Optional[int] = Field(None, ge=1, le=10)


class DrillCreate(DrillBase):
    session_id: int


class DrillUpdate(DrillBase):
    name: Optional[str] = None


class DrillInDBBase(DrillBase):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Drill(DrillInDBBase):
    pass


# Schema for Drill with stats
class DrillWithStats(Drill):
    shot_count: int = 0
    average_accuracy: float = 0.0
    completion_rate: float = 0.0  # Percentage of shots that met target score
