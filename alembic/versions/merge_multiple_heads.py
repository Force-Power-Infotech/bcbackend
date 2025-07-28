"""merge multiple heads

Revision ID: merge_multiple_heads
Revises: add_image_column, fix_drill_groups_schema, update_drill_groups
Create Date: 2025-07-22 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'merge_multiple_heads'
down_revision = ('add_image_column', 'fix_drill_groups_schema', 'update_drill_groups')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
