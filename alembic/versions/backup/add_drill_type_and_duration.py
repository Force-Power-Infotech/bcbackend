"""add drill type and duration

Revision ID: 2023_06_02_drill_fields
Revises: ccb56bbe21f1
Create Date: 2025-06-02 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2023_06_02_drill_fields_merge'
down_revision = ('ccb56bbe21f1', 'add_drill_fields')  # Merge both heads
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add drill_type and duration_minutes columns if they don't exist
    op.execute("""
        DO $$
        BEGIN
            BEGIN
                ALTER TABLE drills ADD COLUMN drill_type VARCHAR;
            EXCEPTION
                WHEN duplicate_column THEN NULL;
            END;
            
            BEGIN
                ALTER TABLE drills ADD COLUMN duration_minutes INTEGER;
            EXCEPTION
                WHEN duplicate_column THEN NULL;
            END;
        END $$;
    """)


def downgrade() -> None:
    # Drop the added columns
    op.execute("""
        DO $$
        BEGIN
            BEGIN
                ALTER TABLE drills DROP COLUMN IF EXISTS drill_type;
            EXCEPTION
                WHEN undefined_column THEN NULL;
            END;
            
            BEGIN
                ALTER TABLE drills DROP COLUMN IF EXISTS duration_minutes;
            EXCEPTION
                WHEN undefined_column THEN NULL;
            END;
        END $$;
    """)
