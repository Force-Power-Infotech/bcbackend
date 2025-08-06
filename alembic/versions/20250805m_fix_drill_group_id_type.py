"""Fix drill_group_id type in practice_sessions table

Revision ID: 20250805m
Revises: 20250805l_fix_practice_sessions_uuid
Create Date: 2025-08-06 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '20250805m'
down_revision = '20250805l'  # Updated to follow the correct sequence
branch_labels = None
depends_on = None


def upgrade():
    # First drop the foreign key constraint if it exists
    op.execute('ALTER TABLE practice_sessions DROP CONSTRAINT IF EXISTS practice_sessions_drill_group_id_fkey')
    
    # Then alter the column type to UUID
    op.execute('ALTER TABLE practice_sessions ALTER COLUMN drill_group_id TYPE UUID USING drill_group_id::uuid')
    
    # Re-add the foreign key constraint
    op.create_foreign_key(
        'practice_sessions_drill_group_id_fkey',
        'practice_sessions',
        'drill_groups',
        ['drill_group_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    # First drop the foreign key constraint
    op.drop_constraint('practice_sessions_drill_group_id_fkey', 'practice_sessions', type_='foreignkey')
    
    # Then convert back to integer (note: this may cause data loss if UUIDs cannot be converted to integers)
    op.execute('ALTER TABLE practice_sessions ALTER COLUMN drill_group_id TYPE INTEGER USING drill_group_id::text::integer')
    
    # Re-add the foreign key constraint
    op.create_foreign_key(
        'practice_sessions_drill_group_id_fkey',
        'practice_sessions',
        'drill_groups',
        ['drill_group_id'],
        ['id'],
        ondelete='CASCADE'
    )
