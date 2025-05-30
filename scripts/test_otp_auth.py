#!/usr/bin/env python
"""
Test script to verify the phone OTP authentication system
"""
import sys
import asyncio
import json
import httpx
from pprint import pprint

# Base URL for local development
BASE_URL = "http://localhost:8000/api/v1"

async def test_request_otp(phone_number):
    """Test requesting an OTP"""
    print(f"\n1. Request OTP for {phone_number}")
    url = f"{BASE_URL}/auth/request-otp"
    payload = {"phone_number": phone_number}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        data = response.json()
        print(f"Status code: {response.status_code}")
        pprint(data)
        
        # In development mode, we should get the OTP back for testing
        otp = data.get("dev_otp")
        if otp:
            print(f"OTP for testing: {otp}")
        else:
            otp = input("Enter the OTP you received (or check console logs): ")
        
        return otp

async def test_verify_otp(phone_number, otp):
    """Test verifying an OTP"""
    print(f"\n2. Verify OTP for {phone_number}")
    url = f"{BASE_URL}/auth/verify-otp"
    payload = {
        "phone_number": phone_number,
        "otp": otp
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        data = response.json()
        print(f"Status code: {response.status_code}")
        pprint(data)
        
        return data.get("user_exists", False)

async def test_register(phone_number, otp):
    """Test completing registration after OTP verification"""
    print(f"\n3. Register a new user with {phone_number}")
    url = f"{BASE_URL}/auth/register/complete"
    payload = {
        "phone_number": phone_number,
        "otp": otp,
        "email": f"test_{phone_number}@example.com",
        "username": f"test_user_{phone_number[-4:]}",
        "password": "securepassword123",
        "full_name": "Test User"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            pprint(data)
            return data
        else:
            print(f"Registration failed: {response.text}")
            return None

async def test_login_with_phone(phone_number, otp):
    """Test logging in with phone and OTP"""
    print(f"\n4. Login with phone {phone_number}")
    url = f"{BASE_URL}/auth/login/phone"
    payload = {
        "phone_number": phone_number,
        "otp": otp
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            pprint(data)
            print(f"Access token received: {data['access_token'][:20]}...")
            return data
        else:
            print(f"Login failed: {response.text}")
            return None

async def main():
    """Run the testing sequence"""
    if len(sys.argv) > 1:
        phone_number = sys.argv[1]
    else:
        phone_number = input("Enter a phone number to test (e.g., 1234567890): ")
    
    # Step 1: Request OTP
    otp = await test_request_otp(phone_number)
    if not otp:
        print("Failed to get OTP.")
        return
    
    # Step 2: Verify OTP
    user_exists = await test_verify_otp(phone_number, otp)
    
    # Step 3 & 4: Either register or login
    if user_exists:
        print(f"\nUser with phone {phone_number} already exists. Will try login.")
        # Request a new OTP for login
        otp = await test_request_otp(phone_number)
        await test_login_with_phone(phone_number, otp)
    else:
        print(f"\nNo user found with phone {phone_number}. Will try registration.")
        # Request a new OTP for registration
        otp = await test_request_otp(phone_number)
        user = await test_register(phone_number, otp)
        if user:
            # Now try logging in
            print("\nUser registered successfully. Now testing login...")
            otp = await test_request_otp(phone_number)
            await test_login_with_phone(phone_number, otp)

if __name__ == "__main__":
    asyncio.run(main())
