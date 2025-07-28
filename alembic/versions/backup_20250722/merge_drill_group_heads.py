"""merge drill group heads

Revision ID: merge_drill_group_heads
Revises: add_drill_group_drills,merge_multiple_heads
Create Date: 2025-06-04 18:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'merge_drill_group_heads'
down_revision = ('add_drill_group_drills', 'merge_multiple_heads')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
