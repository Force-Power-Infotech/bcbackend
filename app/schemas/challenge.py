from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ChallengeStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    COMPLETED = "completed"
    EXPIRED = "expired"


class ChallengeBase(BaseModel):
    title: str
    description: Optional[str] = None
    drill_type: Optional[str] = None
    target_score: Optional[int] = Field(None, ge=1, le=10)


class ChallengeCreate(ChallengeBase):
    recipient_id: int


class ChallengeUpdate(BaseModel):
    status: Optional[ChallengeStatusEnum] = None
    title: Optional[str] = None
    description: Optional[str] = None
    target_score: Optional[int] = Field(None, ge=1, le=10)


class ChallengeInDBBase(ChallengeBase):
    id: int
    sender_id: int
    recipient_id: int
    status: ChallengeStatusEnum
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Challenge(ChallengeInDBBase):
    pass


class ChallengeWithUsers(Challenge):
    sender_username: str
    recipient_username: str
