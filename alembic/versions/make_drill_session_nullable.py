"""make drill session nullable

Revision ID: make_drill_session_nullable
Revises: ccb56bbe21f1
Create Date: 2025-05-31

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccb56bbe21f2'
down_revision = '18ecbfc9ab39'
branch_labels = None
depends_on = None


def upgrade():
    # Make session_id column nullable
    op.alter_column('drills', 'session_id',
                    existing_type=sa.Integer(),
                    nullable=True)


def downgrade():
    # Make session_id column non-nullable
    op.alter_column('drills', 'session_id',
                    existing_type=sa.Integer(),
                    nullable=False)
