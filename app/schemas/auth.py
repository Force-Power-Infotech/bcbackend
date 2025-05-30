from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class PhoneNumberRequest(BaseModel):
    """Schema for requesting OTP to be sent to a phone number"""
    phone_number: str = Field(..., min_length=10, max_length=15)
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Remove any spaces, dashes, or parentheses
        v = ''.join(filter(str.isdigit, v))
        if len(v) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return v


class OTPVerify(BaseModel):
    """Schema for verifying OTP"""
    phone_number: str
    otp: str = Field(..., min_length=6, max_length=6)
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Remove any spaces, dashes, or parentheses
        v = ''.join(filter(str.isdigit, v))
        if len(v) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return v
    
    @validator('otp')
    def validate_otp(cls, v):
        if not v.isdigit():
            raise ValueError('OTP must contain only digits')
        return v


class RegistrationComplete(OTPVerify):
    """Schema for completing registration after OTP verification"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: str = Field(..., min_length=8)
    
    @validator('username')
    def validate_username(cls, v):
        if not all(c.isalnum() or c in ('_', '-', '.') for c in v):
            raise ValueError('Username can only contain alphanumeric characters, underscores, hyphens, and dots')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class LoginComplete(BaseModel):
    """Schema for logging in after OTP verification"""
    phone_number: str
    otp: str = Field(..., min_length=6, max_length=6)
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Remove any spaces, dashes, or parentheses
        v = ''.join(filter(str.isdigit, v))
        if len(v) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return v
    
    @validator('otp')
    def validate_otp(cls, v):
        if not v.isdigit():
            raise ValueError('OTP must contain only digits')
        return v


# For API responses
class PhoneVerificationResponse(BaseModel):
    """Response for phone verification request"""
    message: str
    success: bool


class OTPVerificationResponse(BaseModel):
    """Response for OTP verification"""
    message: str
    success: bool
