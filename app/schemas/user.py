from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime


# Base User Schema
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True
    phone_number: str
    phone_verified: bool = False
    email_verified: bool = False


# Schema for User Creation
class UserCreate(UserBase):
    password: str
    email: EmailStr
    username: str
    phone_number: str = Field(..., min_length=10, max_length=20)

    @validator('password')
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
        
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Remove any spaces, dashes, or parentheses
        if v:
            v = ''.join(filter(str.isdigit, v))
            if len(v) < 10:
                raise ValueError('Phone number must have at least 10 digits')
            if len(v) > 20:
                raise ValueError('Phone number cannot be longer than 20 digits')
        return v


# Schema for User Update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    phone_number: Optional[str] = None
    phone_verified: Optional[bool] = None
    email_verified: Optional[bool] = None


# Schema for User in DB
class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_admin: bool = False

    class Config:
        orm_mode = True


# Schema for displaying User
class User(UserInDBBase):
    pass


# Schema for User with password
class UserInDB(UserInDBBase):
    hashed_password: str


# Schema for token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
