import random
import string
import time
from typing import Dict, Optional

from app.core.config import settings

# Store OTPs with expiration time (in-memory storage, will be lost on restart)
# In production, use Redis or a database to store these
otp_store: Dict[str, Dict[str, any]] = {}

def generate_otp(phone_number: str, length: int = 6) -> str:
    """
    Generate a random numeric OTP of specified length
    """
    # Generate random OTP
    otp = ''.join(random.choices(string.digits, k=length))
    
    # Store OTP with expiration time (5 minutes)
    expiration = time.time() + (5 * 60)  # 5 minutes from now
    otp_store[phone_number] = {
        "otp": otp,
        "expiration": expiration,
        "attempts": 0
    }
    
    return otp

def verify_otp(phone_number: str, otp: str) -> bool:
    """
    Verify if the provided OTP is valid for the given phone number
    """
    # Check if OTP exists for this phone number
    if phone_number not in otp_store:
        return False
    
    stored_data = otp_store[phone_number]
    
    # Check if OTP has expired
    if time.time() > stored_data["expiration"]:
        # Remove expired OTP
        del otp_store[phone_number]
        return False
    
    # Check if too many attempts
    if stored_data["attempts"] >= 3:  # Limit to 3 attempts
        # Remove OTP after too many attempts
        del otp_store[phone_number]
        return False
    
    # Increment attempt counter
    stored_data["attempts"] += 1
    
    # Check if OTP matches
    if stored_data["otp"] == otp:
        # OTP verified, remove it from store
        del otp_store[phone_number]
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
