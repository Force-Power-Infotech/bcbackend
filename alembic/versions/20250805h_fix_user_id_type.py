"""Fix user_id type

Revision ID: 20250805h
Revises: 20250805f
Create Date: 2025-08-05 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250805h'
down_revision = '20250805f'
branch_labels = None
depends_on = None


def upgrade():
    # We'll implement the actual changes in the next migration
    pass


def downgrade():
    pass
