from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

from .drill import Drill


class DrillGroupBase(BaseModel):
    name: str = Field(..., description="Name of the drill group")
    description: Optional[str] = Field(None, description="Description of the drill group")
    image: Optional[str] = Field(None, description="URL of the drill group image")
    meta_drill_group_id: Optional[UUID] = None


class DrillGroupCreate(DrillGroupBase):
    drill_ids: Optional[List[UUID]] = Field(default=[], description="List of drill IDs to add to the group")
    is_public: bool = Field(default=True, description="Whether the drill group is public")
    tags: Optional[List[str]] = Field(default=[], description="Tags for categorizing the drill group")
    difficulty: Optional[str] = Field(default="1", description="Difficulty level of the drill group")
    meta_drill_group_id: Optional[UUID] = None

    @model_validator(mode='before')
    @classmethod
    def validate_difficulty(cls, data):
        if isinstance(data, dict) and 'difficulty' in data:
            if isinstance(data['difficulty'], int):
                data['difficulty'] = str(data['difficulty'])
            elif data['difficulty'] is None:
                data['difficulty'] = "1"
        return data


class DrillGroupUpdate(DrillGroupBase):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    meta_drill_group_id: Optional[UUID] = None


class DrillGroupInDBBase(DrillGroupBase):
    id: UUID
    user_id: Optional[int] = Field(default=1)  # Default to user ID 1
    is_public: bool = Field(default=True)
    difficulty: Optional[str] = Field(default="1")
    tags: Optional[List[str]] = Field(default=[])
    created_at: datetime
    updated_at: Optional[datetime] = None
    meta_drill_group_id: Optional[UUID] = None

    class Config:
        from_attributes = True

    def __init__(self, **data):
        if 'difficulty' in data:
            if isinstance(data['difficulty'], int):
                data['difficulty'] = str(data['difficulty'])
            elif data['difficulty'] is None:
                data['difficulty'] = "1"
            elif isinstance(data['difficulty'], str):
                # Ensure it's a valid integer string
                try:
                    int(data['difficulty'])
                except ValueError:
                    data['difficulty'] = "1"
        else:
            data['difficulty'] = "1"
        super().__init__(**data)


class DrillGroup(DrillGroupInDBBase):
    drills: Optional[List[Drill]] = Field(default=[])
    
    @property
    def difficulty(self) -> str:
        return str(self._difficulty) if self._difficulty else "1"
    
    @difficulty.setter
    def difficulty(self, value: Optional[int]):
        self._difficulty = value if value is not None else 1
