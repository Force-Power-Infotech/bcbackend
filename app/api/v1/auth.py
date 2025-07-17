from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.db.base import get_db
from app.db.models.user import User as UserModel
from app.schemas.user import User, UserCreate
from app.crud import crud_user
from app.api import deps
from app.schemas.auth import PhoneNumberRequest, OTPVerify, PhoneVerificationResponse, OTPVerificationResponse

router = APIRouter()

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Log in user and set session
    """
    user = await crud_user.authenticate(db, username=username, password=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Set session data
    request.session["username"] = user.username
    request.session["user_id"] = user.id
    
    return {
        "status": "success",
        "message": "Successfully logged in",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_admin": user.is_admin
        }
    }

@router.post("/register", response_model=User)
async def register_user(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Register a new user.
    """
    # Check if user with this email already exists
    user = await crud_user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    
    # Check if user with this username already exists
    user = await crud_user.get_by_username(db, username=username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists",
        )
    
    # Create new user
    user_in = UserCreate(
        email=email,
        username=username,
        password=password,
        full_name=full_name
    )
    user = await crud_user.create(db, obj_in=user_in)
    return user

@router.post("/logout")
async def logout(request: Request):
    """
    Log out user by clearing session
    """
    request.session.clear()
    return {"status": "success", "message": "Successfully logged out"}

@router.post(
    "/request-otp",
    response_model=PhoneVerificationResponse,
    tags=["auth"],
    summary="Request OTP for login/registration"
)
async def request_otp(
    payload: PhoneNumberRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Request OTP for login/registration.
    """
    phone_number = payload.phone_number
    static_otp = "0000"
    user = await crud_user.get_by_phone(db, phone_number=phone_number)
    if user:
        await crud_user.update_otp(db, user=user, otp=static_otp)
    else:
        user_data = UserCreate(
            email=f"temp_{phone_number}@temp.com",
            username=f"temp_{phone_number}",
            password="temp_password",
            phone_number=phone_number,
            full_name="Temporary User"
        )
        user = await crud_user.create(db, obj_in=user_data)
        await crud_user.update_otp(db, user=user, otp=static_otp)
    return {"message": "OTP sent successfully", "success": True}

@router.post(
    "/verify-otp",
    response_model=OTPVerificationResponse,
    tags=["auth"],
    summary="Verify OTP and return user status"
)
async def verify_otp(
    request: Request,
    verify_data: OTPVerify,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Verify OTP and return user status.
    """
    user = await crud_user.get_by_phone(db, phone_number=verify_data.phone_number)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.otp == verify_data.otp:
        await crud_user.update_otp(db, user=user, otp=None)
        is_new_user = user.username.startswith("temp_")
        return {
            "message": "OTP verified successfully",
            "success": True,
            "is_new_user": is_new_user,
            "user_data": {
                "id": user.id,
                "phone_number": user.phone_number,
                "username": None if is_new_user else user.username,
                "email": None if is_new_user else user.email
            }
        }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid OTP"
    )
