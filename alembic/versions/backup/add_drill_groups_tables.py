"""add drill groups tables

Revision ID: 2023_add_drill_groups
Revises: ccb56bbe21f1
Create Date: 2025-06-02 17:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2023_add_drill_groups'
down_revision = 'ccb56bbe21f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create drill_groups table
    op.create_table(
        'drill_groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create drill_group_drills association table
    op.create_table(
        'drill_group_drills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('drill_group_id', sa.Integer(), nullable=False),
        sa.Column('drill_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['drill_group_id'], ['drill_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['drill_id'], ['drills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_drill_groups_user_id', 'drill_groups', ['user_id'])
    op.create_index('ix_drill_group_drills_drill_group_id', 'drill_group_drills', ['drill_group_id'])
    op.create_index('ix_drill_group_drills_drill_id', 'drill_group_drills', ['drill_id'])


def downgrade() -> None:
    op.drop_table('drill_group_drills')
    op.drop_table('drill_groups')
