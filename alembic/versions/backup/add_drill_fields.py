"""add drill type and duration

Revision ID: add_drill_fields
Revises: ccb56bbe21f2
Create Date: 2025-06-02 11:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_drill_fields'
down_revision = 'ccb56bbe21f2'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns
    op.add_column('drills', sa.Column('drill_type', sa.String(), nullable=True))
    op.add_column('drills', sa.Column('duration_minutes', sa.Integer(), nullable=True))

    # Update existing rows with default values
    op.execute("UPDATE drills SET drill_type = 'DRAW' WHERE drill_type IS NULL")
    op.execute("UPDATE drills SET duration_minutes = 30 WHERE duration_minutes IS NULL")

    # Make columns non-nullable after setting defaults
    op.alter_column('drills', 'drill_type',
                    existing_type=sa.String(),
                    nullable=False)
    op.alter_column('drills', 'duration_minutes',
                    existing_type=sa.Integer(),
                    nullable=False)
