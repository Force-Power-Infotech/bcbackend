from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class PracticeSessionCreate(BaseModel):
    drill_group_id: int
    drill_ids: List[int]
    user_id: int


from app.schemas.drill import Drill
from app.schemas.drill_group import DrillGroup
from app.schemas.user import User


class PracticeSessionResponse(BaseModel):
    id: int
    user_id: int
    drill_group_id: int
    drill_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PracticeSessionDetailResponse(BaseModel):
    id: int
    user_id: int
    drill_group_id: int
    drill_id: int
    created_at: datetime
    drill: Optional[Drill] = None
    drill_group: Optional[DrillGroup] = None
    user: Optional[User] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [{
                "drill": {"difficulty": "1"},
                "drill_group": {"difficulty": "1"}
            }]
        }
    }

    @model_validator(mode='before')
    @classmethod
    def validate_difficulties(cls, data):
        if isinstance(data, dict):
            if 'drill' in data and isinstance(data['drill'], dict):
                if 'difficulty' in data['drill']:
                    data['drill']['difficulty'] = str(data['drill']['difficulty'])
            if 'drill_group' in data and isinstance(data['drill_group'], dict):
                if 'difficulty' in data['drill_group']:
                    data['drill_group']['difficulty'] = str(data['drill_group']['difficulty'])
        return data


class PracticeSessionBulkResponse(BaseModel):
    practice_sessions: List[PracticeSessionResponse]
    message: str
