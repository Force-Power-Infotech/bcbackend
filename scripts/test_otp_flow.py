import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import engine, async_session
from app.utils.otp import generate_otp, verify_otp
from app.crud import crud_user
from app.schemas.user import UserCreate

async def test_otp_flow():
    """
    Test the complete OTP flow:
    1. Generate an OTP for a phone number
    2. Store it in the database
    3. Verify the OTP
    """
    print("Starting OTP flow test...")
    
    # Create a database session
    async with async_session() as session:
        # Use phone number for testing
        phone_number = "+1234567890"
        
        # Check if test user exists, create if not
        user = await crud_user.get_by_phone(session, phone_number=phone_number)
        if not user:
            print(f"Creating test user with phone {phone_number}...")
            user_data = UserCreate(
                email="test@example.com",
                username="testuser",
                password="password123",
                phone_number=phone_number,
                full_name="Test User"
            )
            user = await crud_user.create(session, obj_in=user_data)
            print(f"Created test user: {user.username} (ID: {user.id})")
        else:
            print(f"Using existing user: {user.username} (ID: {user.id})")
        
        # Generate OTP
        print("Generating OTP...")
        otp = await generate_otp(session, phone_number)
        print(f"Generated OTP: {otp}")
        
        # Retrieve user to check OTP was stored
        user = await crud_user.get_by_phone(session, phone_number=phone_number)
        print(f"User OTP in database: {user.otp}")
        
        # Verify correct OTP
        print("\nTesting correct OTP verification...")
        is_valid = await verify_otp(session, phone_number, otp)
        print(f"OTP verification result: {'Success' if is_valid else 'Failed'}")
        
        # Verify incorrect OTP
        print("\nTesting incorrect OTP verification...")
        is_valid = await verify_otp(session, phone_number, "000000")
        print(f"Incorrect OTP verification result: {'Incorrectly succeeded' if is_valid else 'Correctly failed'}")
        
        print("\nOTP flow test complete!")


if __name__ == "__main__":
    asyncio.run(test_otp_flow())
