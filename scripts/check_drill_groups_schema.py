"""Check drill_groups table schema

This script connects to the database and checks the schema of the drill_groups table
to ensure our migrations worked correctly.
"""
import asyncio
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import settings

async def check_drill_groups_schema():
    # Create engine and connect
    engine = create_async_engine(settings.DATABASE_URL)
    
    async with engine.begin() as conn:
        # Get inspector
        inspector = inspect(conn)
        
        # Check table columns
        columns = await conn.run_sync(lambda sync_conn: inspector.get_columns("drill_groups"))
        
        print("Drill Groups Table Columns:")
        for column in columns:
            print(f"- {column['name']}: {column['type']} (nullable: {column.get('nullable', 'unknown')})")
            
        # Check if our new columns exist
        result = await conn.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drill_groups' AND column_name='is_public')"))
        has_is_public = await result.scalar()
        print(f"\nHas is_public column: {has_is_public}")
        
        result = await conn.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drill_groups' AND column_name='difficulty')"))
        has_difficulty = await result.scalar()
        print(f"Has difficulty column: {has_difficulty}")
        
        result = await conn.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drill_groups' AND column_name='tags')"))
        has_tags = await result.scalar()
        print(f"Has tags column: {has_tags}")

if __name__ == "__main__":
    asyncio.run(check_drill_groups_schema())
