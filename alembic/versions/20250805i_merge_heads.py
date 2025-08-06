"""Merge migration heads

Revision ID: 20250805i
Revises: 20250805h
Create Date: 2025-08-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250805i'
down_revision = '20250805h'
branch_labels = None
depends_on = None


def upgrade():
    # This is a merge migration
    pass


def downgrade():
    pass
