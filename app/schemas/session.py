from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None


class SessionCreate(SessionBase):
    pass


class SessionUpdate(SessionBase):
    title: Optional[str] = None


class SessionInDBBase(SessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Session(SessionInDBBase):
    pass


# Schema for Session with stats
class SessionWithStats(Session):
    shot_count: int = 0
    average_accuracy: float = 0.0
    drill_count: int = 0
