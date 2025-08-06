"""Fix column types

Revision ID: 20250805j
Revises: 20250805i
Create Date: 2025-08-05 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250805j'
down_revision = '20250805i'
branch_labels = None
depends_on = None


def upgrade():
    # We'll implement the actual changes in the next migration
    pass


def downgrade():
    pass
