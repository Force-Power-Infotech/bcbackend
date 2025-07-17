"""Rename drills type column to drill_type

Revision ID: rename_type_to_drill_type
Revises: update_drills_schema
Create Date: 2025-06-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'rename_type_to_drill_type'
down_revision = 'update_drills_schema'
branch_labels = None
depends_on = None


def upgrade():
    # First make drill_type not nullable since we'll copy data to it
    op.alter_column('drills', 'drill_type',
                    existing_type=sa.String(length=50),
                    nullable=False)
    
    # Copy data from type to drill_type
    op.execute('UPDATE drills SET drill_type = type')
    
    # Drop the type column
    op.drop_column('drills', 'type')


def downgrade():
    # Add back the type column
    op.add_column('drills', sa.Column('type', sa.String(length=50), nullable=True))
    
    # Copy data from drill_type to type
    op.execute('UPDATE drills SET type = drill_type')
    
    # Make type not nullable
    op.alter_column('drills', 'type',
                    existing_type=sa.String(length=50),
                    nullable=False)
