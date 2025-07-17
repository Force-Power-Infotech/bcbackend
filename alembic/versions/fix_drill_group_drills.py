"""Fix drill_group_drills table

Revision ID: fix_drill_group_drills
Revises: create_shots_table
Create Date: 2025-06-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fix_drill_group_drills'
down_revision = 'create_shots_table'
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign keys first
    op.drop_constraint('drill_group_drills_drill_group_id_fkey', 'drill_group_drills', type_='foreignkey')
    op.drop_constraint('drill_group_drills_drill_id_fkey', 'drill_group_drills', type_='foreignkey')
    
    # Drop indexes if they exist
    try:
        op.drop_index('idx_drill_group_drills_drill_id', table_name='drill_group_drills')
    except:
        pass
    try:
        op.drop_index('idx_drill_group_drills_group_id', table_name='drill_group_drills')
    except:
        pass
    
    # Drop the table
    op.drop_table('drill_group_drills')

    # Create the new table with correct structure
    op.create_table(
        'drill_group_drills',
        sa.Column('drill_group_id', sa.Integer(), nullable=False),
        sa.Column('drill_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['drill_group_id'], ['drill_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['drill_id'], ['drills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('drill_group_id', 'drill_id')
    )
    
    # Create indexes for better performance
    op.create_index(
        'idx_drill_group_drills_drill_id',
        'drill_group_drills',
        ['drill_id']
    )
    op.create_index(
        'idx_drill_group_drills_group_id',
        'drill_group_drills',
        ['drill_group_id']
    )

    # We don't need to migrate data as the table is empty


def downgrade():
    # Drop the new table structure
    op.drop_index('idx_drill_group_drills_group_id', table_name='drill_group_drills')
    op.drop_index('idx_drill_group_drills_drill_id', table_name='drill_group_drills')
    op.drop_table('drill_group_drills')

    # Create the old table structure
    op.create_table(
        'drill_group_drills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('drill_group_id', sa.Integer(), nullable=False),
        sa.Column('drill_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['drill_group_id'], ['drill_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['drill_id'], ['drills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
