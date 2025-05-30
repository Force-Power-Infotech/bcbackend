from typing import Any, AsyncGenerator, Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import settings

# Create SQLAlchemy base
Base = declarative_base()

# Check if we're using psycopg2 (sync) or asyncpg (async)
if 'psycopg2' in settings.DATABASE_URL:
    use_async = False
    db_url = settings.DATABASE_URL
    
    # Create sync engine for the database
    engine = create_engine(
        db_url,
        echo=True,
        future=True,
    )
    
    # Create sync session factory
    sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    use_async = True
    # Ensure we have an asyncpg URL for async connections
    if 'asyncpg' not in settings.DATABASE_URL:
        # Convert standard postgresql:// to postgresql+asyncpg://
        db_url = settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
    else:
        db_url = settings.DATABASE_URL
    
    # Create async engine for the database
    engine = create_async_engine(
        db_url,
        echo=True,
        future=True,
    )
    
    # Create async session factory
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[Any, None]:
    """
    Dependency for getting database sessions (either async or sync)
    """
    if use_async:
        # Use async session for asyncpg
        async with async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    else:
        # For sync connections, use sync session but yield it like an async session
        # This allows the same endpoints to work with both connection types
        db = sync_session()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
