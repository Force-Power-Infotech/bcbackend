from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class DrillBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_score: int = Field(default=80, ge=0, le=100, description="Target score (0-100)")
    difficulty: str = Field(default="1", description="Difficulty level (1-5)")
    drill_type: str = Field(description="Type of drill (DRAW, DRIVE, etc.)")
    duration_minutes: int = Field(default=30, ge=5, le=120, description="Duration in minutes")

    model_config = {
        "json_schema_extra": {
            "examples": [{"difficulty": "1"}]
        }
    }
    
    @model_validator(mode='before')
    @classmethod
    def validate_difficulty(cls, data):
        if isinstance(data, dict) and 'difficulty' in data:
            if isinstance(data['difficulty'], int):
                data['difficulty'] = str(data['difficulty'])
        return data


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

    def __init__(self, **data):
        super().__init__(**data)
        if hasattr(self, 'difficulty'):
            self._difficulty = self.difficulty
            self.difficulty = str(self._difficulty)


class Drill(DrillInDBBase):
    @property
    def difficulty(self) -> str:
        return str(self._difficulty)
    
    @difficulty.setter
    def difficulty(self, value: int):
        self._difficulty = value


# Schema for Drill with stats
class DrillWithStats(Drill):
    shot_count: int = 0
    average_accuracy: float = 0.0
    completion_rate: float = 0.0  # Percentage of shots that met target score
