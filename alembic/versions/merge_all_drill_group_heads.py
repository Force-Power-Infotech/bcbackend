"""merge all drill group heads

Revision ID: merge_all_drill_group_heads
Revises: fix_drill_groups_schema, merge_drill_group_heads, update_drill_groups
Create Date: 2025-06-04 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'merge_all_drill_group_heads'
down_revision = ('fix_drill_groups_schema', 'merge_drill_group_heads', 'update_drill_groups')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
