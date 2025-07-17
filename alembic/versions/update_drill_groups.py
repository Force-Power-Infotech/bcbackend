"""update drill groups and relationships

Revision ID: update_drill_groups
Revises: update_drills_schema
Create Date: 2025-06-04 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'update_drill_groups'
down_revision = 'update_drills_schema'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_public column to drill_groups table
    op.add_column('drill_groups', sa.Column('is_public', sa.Boolean(), nullable=False, server_default='false'))

    # Create drill_group_drills association table
    op.create_table(
        'drill_group_drills',
        sa.Column('drill_group_id', sa.Integer(), nullable=False),
        sa.Column('drill_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['drill_group_id'], ['drill_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['drill_id'], ['drills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('drill_group_id', 'drill_id')
    )

    # Create index for faster lookups
    op.create_index(
        'ix_drill_group_drills_drill_group_id',
        'drill_group_drills',
        ['drill_group_id']
    )
    op.create_index(
        'ix_drill_group_drills_drill_id',
        'drill_group_drills',
        ['drill_id']
    )


def downgrade():
    # Drop indexes
    op.drop_index('ix_drill_group_drills_drill_id')
    op.drop_index('ix_drill_group_drills_drill_group_id')

    # Drop drill_group_drills table
    op.drop_table('drill_group_drills')

    # Drop is_public column from drill_groups
    op.drop_column('drill_groups', 'is_public')
