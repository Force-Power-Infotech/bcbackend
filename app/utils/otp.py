import random
import string
import time
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import crud_user

# Store OTPs with expiration time (in-memory storage, will be lost on restart)
# In production, use Redis or a database to store these
otp_store: Dict[str, Dict[str, any]] = {}

async def generate_otp(db: AsyncSession, phone_number: str, length: int = 6) -> str:
    """
    Generate a random numeric OTP of specified length and store it in the database.
    """
    # Generate random OTP
    otp = ''.join(random.choices(string.digits, k=length))
    
    # Store OTP in the user's record in the database
    user = await crud_user.get_by_phone(db, phone_number=phone_number)
    if user:
        await crud_user.update_otp(db, user=user, otp=otp)
    
    # For development, also store in memory
    otp_store[phone_number] = {
        "otp": otp,
        "expiration": time.time() + (settings.OTP_EXPIRY_SECONDS if hasattr(settings, 'OTP_EXPIRY_SECONDS') else 600)
    }
    
    print(f"Generated OTP {otp} for {phone_number}")
    return otp

async def verify_otp(db: AsyncSession, phone_number: str, otp: str) -> bool:
    """
    Verify the OTP against what's stored in the database.
    """
    print(f"Verifying OTP {otp} for {phone_number}")
    
    # Check database first
    user = await crud_user.get_by_phone(db, phone_number=phone_number)
    if user and user.otp == otp:
        # Clear the OTP after successful verification
        await crud_user.update_otp(db, user=user, otp=None)
        return True
    
    # Fallback to in-memory store for testing
    if phone_number in otp_store:
        stored = otp_store[phone_number]
        if stored["otp"] == otp and time.time() <= stored["expiration"]:
            otp_store.pop(phone_number, None)  # Remove after successful verification
            return True
    
    return False

def mock_send_otp(phone_number: str, otp: str) -> bool:
    """
    Mock function to simulate sending OTP via SMS
    In production, this would integrate with an SMS API provider
    """
    # For development, just print the OTP
    print(f"Sending OTP {otp} to {phone_number}")
    return True

def get_stored_otp(phone_number: str) -> Optional[str]:
    """
    Get the stored OTP for a phone number (for debugging purposes only)
    """
    if phone_number in otp_store and time.time() <= otp_store[phone_number]["expiration"]:
        return otp_store[phone_number]["otp"]
    return None
