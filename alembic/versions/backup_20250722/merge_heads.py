"""merge heads

Revision ID: merge_multiple_heads
Revises: a1,add_is_public_column
Create Date: 2025-06-04 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'merge_multiple_heads'
down_revision = ('a1', 'add_is_public_column')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
