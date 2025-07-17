"""Add session_id foreign key to drills

Revision ID: add_session_id_fkey
Revises: create_sessions_table
Create Date: 2025-06-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_session_id_fkey'
down_revision = 'create_sessions_table'
branch_labels = None
depends_on = None


def upgrade():
    # Create the foreign key constraint
    op.create_foreign_key(
        'fk_drills_session_id',
        'drills', 'sessions',
        ['session_id'], ['id'],
        ondelete='CASCADE'
    )
    # Create an index for better performance
    op.create_index(
        op.f('ix_drills_session_id'),
        'drills', ['session_id'],
        unique=False
    )


def downgrade():
    op.drop_index(op.f('ix_drills_session_id'), table_name='drills')
    op.drop_constraint('fk_drills_session_id', 'drills', type_='foreignkey')
