"""Add is_public column to drill_groups

Revision ID: add_is_public_column
Revises: add_phone_columns_fix
Create Date: 2025-06-04 17:56:42.052

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_is_public_column'
down_revision = 'add_phone_columns_fix'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_public column as nullable first
    op.add_column('drill_groups', sa.Column('is_public', sa.Boolean(), nullable=True))
    
    # Set all existing rows to True (making them public by default)
    op.execute("UPDATE drill_groups SET is_public = TRUE")
    
    # Now make the column non-nullable with default
    op.alter_column('drill_groups', 'is_public',
                    existing_type=sa.Boolean(),
                    nullable=False,
                    server_default=sa.text('true'))


def downgrade():
    op.drop_column('drill_groups', 'is_public')
