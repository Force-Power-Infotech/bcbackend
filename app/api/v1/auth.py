from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from app.core.config import settings
from app.core.security import create_access_token
from app.db.base import get_db
from app.db.models.user import User as UserModel
from app.schemas.user import User, UserCreate, Token
from app.schemas.auth import (
    PhoneNumberRequest, OTPVerify, RegistrationComplete, 
    LoginComplete, PhoneVerificationResponse, OTPVerificationResponse
)
from app.crud import crud_user
from app.utils.otp import generate_otp as db_generate_otp, verify_otp as db_verify_otp, mock_send_otp
from app.utils.email import send_verification_email

router = APIRouter()


@router.post("/register", response_model=User)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Register a new user.
    """
    # Check if user with this email already exists
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    
    # Check if user with this username already exists
    user = await crud_user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists",
        )
    
    # Check if user with this phone number already exists
    user = await crud_user.get_by_phone(db, phone_number=user_in.phone_number)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this phone number already exists",
        )
    
    # Create new user
    user = await crud_user.create(db, obj_in=user_in)
    return user


@router.post("/request-otp", response_model=PhoneVerificationResponse)
async def request_otp(
    phone_req: PhoneNumberRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Request an OTP to be sent to the phone number
    """
    phone_number = phone_req.phone_number

    # Generate and send OTP
    otp = await db_generate_otp(db, phone_number)

    # In production, use an actual SMS service
    mock_send_otp(phone_number, otp)

    return {
        "message": f"OTP sent to {phone_number}",
        "success": True
    }


@router.post("/verify-otp", response_model=OTPVerificationResponse)
async def verify_phone_otp(
    otp_data: OTPVerify,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Verify the OTP sent to the phone number
    """
    phone_number = otp_data.phone_number
    otp_code = otp_data.otp

    is_valid = await db_verify_otp(db, phone_number, otp_code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    return {
        "message": "OTP verified successfully",
        "success": True
    }



@router.post("/login", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    Get an access token for future requests.
    """
    user = await crud_user.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register/complete", response_model=User)
async def complete_registration(
    registration_data: RegistrationComplete,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Complete user registration after OTP verification
    """
    # First verify the OTP again
    phone_number = registration_data.phone_number
    otp_code = registration_data.otp
    
    # Verify OTP
    is_valid = await db_verify_otp(db, phone_number, otp_code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Check if user already exists
    user = await crud_user.get_by_phone(db, phone_number=phone_number)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this phone number already exists"
        )
    
    # Check if email exists
    user = await crud_user.get_by_email(db, email=registration_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Check if username exists
    user = await crud_user.get_by_username(db, username=registration_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )
    
    # Create new user
    user_in = UserCreate(
        email=registration_data.email,
        username=registration_data.username,
        password=registration_data.password,
        phone_number=phone_number,
        full_name=registration_data.full_name,
    )
    user = await crud_user.create(db, obj_in=user_in)
    
    # Mark phone as verified since OTP was validated
    user = await crud_user.mark_phone_verified(db, user=user)
    
    # Send email verification if email service is configured
    if settings.EMAILS_ENABLED:
        await send_verification_email(email_to=user.email)
    
    return user
