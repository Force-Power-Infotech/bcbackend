"""merge_all_heads

Revision ID: c166183ec8ca
Revises: 001_create_users, add_image_column
Create Date: 2025-07-18 06:58:36.686289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c166183ec8ca'
down_revision = ('001_create_users', 'add_image_column')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
