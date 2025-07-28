"""Add image column to drill_groups

Revision ID: add_image_column
Revises: add_is_public_column
Create Date: 2025-06-05 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_image_column'
down_revision = 'add_is_public_column'
branch_labels = None
depends_on = None


def upgrade():
    # Add image column to drill_groups table
    op.add_column('drill_groups',
                 sa.Column('image', sa.String(255), nullable=True))


def downgrade():
    # Drop image column from drill_groups table
    op.drop_column('drill_groups', 'image')
