"""add phone columns fix

Revision ID: add_phone_columns_fix
Revises: initial_setup_001
Create Date: 2025-06-03 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_phone_columns_fix'
down_revision = 'initial_setup_001'
branch_labels = None
depends_on = None


def upgrade():
    # Skip adding columns as they are already included in the initial migration
    pass


def downgrade():
    # Skip dropping columns as they are managed by the initial migration
    pass
