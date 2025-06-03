"""merge_all_heads

Revision ID: 6702227ebfb8
Revises: 208399a6ccc8, add_phone_columns_fix
Create Date: 2025-06-03 16:49:39.454328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6702227ebfb8'
down_revision = ('208399a6ccc8', 'add_phone_columns_fix')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
