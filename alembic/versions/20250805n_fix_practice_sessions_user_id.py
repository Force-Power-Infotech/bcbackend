"""Fix practice_sessions user_id and column types

Revision ID: 20250805n
Revises: 20250805m
Create Date: 2025-08-06 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '20250805n'
down_revision = '20250805m'
branch_labels = None
depends_on = None


def upgrade():
    # Cast column types correctly
    op.execute("""
        BEGIN;
        -- First drop foreign key constraints
        ALTER TABLE practice_sessions DROP CONSTRAINT IF EXISTS practice_sessions_user_id_fkey;
        
        -- Ensure user_id is INTEGER
        ALTER TABLE practice_sessions ALTER COLUMN user_id TYPE INTEGER USING user_id::TEXT::INTEGER;
        
        -- Re-add the foreign key constraint
        ALTER TABLE practice_sessions ADD CONSTRAINT practice_sessions_user_id_fkey 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
            
        -- Make sure drill_id is UUID
        ALTER TABLE practice_sessions ALTER COLUMN drill_id TYPE UUID USING drill_id::UUID;
        
        -- Make sure drill_group_id is UUID
        ALTER TABLE practice_sessions ALTER COLUMN drill_group_id TYPE UUID USING drill_group_id::UUID;
        COMMIT;
    """)


def downgrade():
    # If needed to revert, though this would be dangerous as it might lose data
    op.execute("""
        BEGIN;
        -- Drop foreign key constraints first
        ALTER TABLE practice_sessions DROP CONSTRAINT IF EXISTS practice_sessions_user_id_fkey;
        
        -- Convert columns back
        ALTER TABLE practice_sessions ALTER COLUMN user_id TYPE UUID USING user_id::TEXT::UUID;
        
        -- Re-add constraints
        ALTER TABLE practice_sessions ADD CONSTRAINT practice_sessions_user_id_fkey 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
        COMMIT;
    """)
