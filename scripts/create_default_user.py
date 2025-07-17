import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.db.models.user import User
from app.core.security import get_password_hash

# Create async database engine
engine = create_async_engine("postgresql+asyncpg://postgres:postgres@db:5432/bowlsacedb")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_default_user():
    async with AsyncSessionLocal() as db:
        try:
            # Check if default user exists
            result = await db.execute(select(User).filter(User.id == 1))
            default_user = result.scalar_one_or_none()
            
            if not default_user:
                default_user = User(
                    id=1,
                    email="default@example.com",
                    username="default",
                    hashed_password=get_password_hash("default"),
                    phone_number="1234567890",
                    phone_verified=True,
                    email_verified=True,
                    full_name="Default User",
                    is_active=True,
                    is_admin=True
                )
                db.add(default_user)
                await db.commit()
                print("Created default user")
            else:
                print("Default user already exists")
        except Exception as e:
            print(f"Error creating default user: {e}")
            await db.rollback()
            raise

async def main():
    await create_default_user()

if __name__ == "__main__":
    asyncio.run(main())
