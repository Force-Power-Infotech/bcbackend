"""merge_multiple_heads

Revision ID: 208399a6ccc8
Revises: 725b1936a2ca, add_drill_group_fields
Create Date: 2025-06-03 16:42:39.009626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '208399a6ccc8'
down_revision = ('725b1936a2ca', 'add_drill_group_fields')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
