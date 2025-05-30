from app.schemas.auth import OTPVerify
from app.utils.otp import verify_otp
from app.crud import crud_user
from app.db.base import get_db
import asyncio

# Simulate request payload
def test_verify_otp():
    payload = {
        "phone_number": "1234567890",
        "otp": "029486"
    }

    try:
        # Validate payload against schema
        otp_data = OTPVerify(**payload)
        print("Payload is valid:", otp_data)

        # Simulate OTP verification
        is_valid = verify_otp(otp_data.phone_number, otp_data.otp)
        print("OTP is valid:", is_valid)

        # Simulate database operation
        async def db_operation():
            async for db in get_db():
                user = await crud_user.get_by_phone(db, phone_number=otp_data.phone_number)
                print("User fetched from DB:", user)

        asyncio.run(db_operation())

    except Exception as e:
        print("Error during verification:", str(e))

if __name__ == "__main__":
    test_verify_otp()
