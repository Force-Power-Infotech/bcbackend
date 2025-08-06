"""Fix practice sessions foreign keys

Revision ID: 20250805f
Revises: 3a9110d900cb
Create Date: 2025-08-05 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '20250805f'
down_revision = '3a9110d900cb'
branch_labels = None
depends_on = None


def upgrade():
    # We'll implement the actual changes in the next migration
    pass


def downgrade():
    pass
