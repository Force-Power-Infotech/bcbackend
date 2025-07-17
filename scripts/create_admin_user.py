"""
Script to create the first admin user
Run with: python -m scripts.create_admin_user
"""
import asyncio
import sys
import os

sys.path.append(".")

from app.schemas.user import UserCreate
from app.crud.crud_user import create, get_by_email, update
from app.db.base import Base, engine, get_db, async_session


async def create_admin_user():
    print("Creating first admin user")
    
    # Use environment variables or defaults
    email = os.getenv("ADMIN_EMAIL", "admin@bowlsace.com")
    username = os.getenv("ADMIN_USERNAME", "admin")
    full_name = os.getenv("ADMIN_FULL_NAME", "Admin User")
    password = os.getenv("ADMIN_PASSWORD", "adminpassword123")
    
    async with async_session() as db:
        # Check if user exists
        existing_user = await get_by_email(db, email)
        if existing_user:
            print(f"User with email {email} already exists.")
            make_admin = input("Do you want to make this user an admin? (y/n): ")
            if make_admin.lower() == "y":
                await update(db, db_obj=existing_user, obj_in={"is_admin": True})
                print(f"User {email} is now an admin")
            return
        
        # Create user
        user_create = UserCreate(
            email=email,
            username=username,
            password=password,
            full_name=full_name,
            is_active=True
        )
        
        user = await create(db, obj_in=user_create)
        
        # Make user admin
        await update(db, db_obj=user, obj_in={"is_admin": True})
        
        print(f"Admin user {email} created successfully")


async def main():
    # Create database tables if they don't exist
    async with engine.begin() as conn:
        # Uncomment this line if you want this script to create tables
        # await conn.run_sync(Base.metadata.create_all)
        pass
    
    await create_admin_user()


if __name__ == "__main__":
    asyncio.run(main())
