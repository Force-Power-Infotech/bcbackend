"""Add drill_group_drills association table

Revision ID: add_drill_group_drills
Revises: add_drill_group_columns
Create Date: 2025-06-04 18:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_drill_group_drills'
down_revision = 'add_drill_group_columns'
branch_labels = None
depends_on = None


def upgrade():
    # Create the drill_group_drills association table
    op.create_table(
        'drill_group_drills',
        sa.Column('drill_group_id', sa.Integer(), nullable=False),
        sa.Column('drill_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['drill_group_id'], ['drill_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['drill_id'], ['drills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('drill_group_id', 'drill_id'),
        sa.Index('idx_drill_group_drills_group_id', 'drill_group_id'),
        sa.Index('idx_drill_group_drills_drill_id', 'drill_id')
    )


def downgrade():
    op.drop_table('drill_group_drills')
