"""add session_id to drills

Revision ID: add_session_id_to_drills
Revises: c166183ec8ca
Create Date: 2025-07-21 06:28:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_session_id_to_drills'
down_revision = 'c166183ec8ca'
branch_labels = None
depends_on = None


def upgrade():
    # Add session_id column
    op.add_column('drills', sa.Column('session_id', sa.Integer(), nullable=True))
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_drills_session_id',
        'drills', 'practice_sessions',
        ['session_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade():
    # Remove foreign key constraint
    op.drop_constraint('fk_drills_session_id', 'drills', type_='foreignkey')
    # Remove session_id column
    op.drop_column('drills', 'session_id')
