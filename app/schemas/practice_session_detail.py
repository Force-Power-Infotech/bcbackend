from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class DrillDetail(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    drill_type: Optional[str] = None
    duration_minutes: Optional[int] = None
    target_score: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DrillGroupDetail(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_public: bool
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    drills: List[DrillDetail]

    class Config:
        from_attributes = True


class UserDetail(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool
    phone_verified: bool
    email_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PracticeSessionDetailResponse(BaseModel):
    id: int
    user_id: int
    drill_group_id: int
    drill_id: int
    created_at: datetime
    drill: DrillDetail
    drill_group: DrillGroupDetail
    user: UserDetail

    class Config:
        from_attributes = True
