from pydantic import BaseModel, Field
from typing import Optional, List
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

    class Config:
        from_attributes = True


class PracticeSessionBulkResponse(BaseModel):
    practice_sessions: List[PracticeSessionResponse]
    message: str
