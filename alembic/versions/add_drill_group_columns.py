"""Add tags and difficulty columns to drill_groups

Revision ID: add_drill_group_columns
Revises: add_is_public_column
Create Date: 2025-06-04 18:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_drill_group_columns'
down_revision = 'add_is_public_column'
branch_labels = None
depends_on = None


def upgrade():
    # Add tags column
    op.add_column('drill_groups', sa.Column('tags', sa.JSON(), nullable=True, server_default='[]'))
    
    # Add difficulty column
    op.add_column('drill_groups', sa.Column('difficulty', sa.Integer(), nullable=True, server_default='1'))
    
    # Update existing rows to have default values
    op.execute("UPDATE drill_groups SET tags = '[]' WHERE tags IS NULL")
    op.execute("UPDATE drill_groups SET difficulty = 1 WHERE difficulty IS NULL")
    
    # Make difficulty non-nullable after setting defaults
    op.alter_column('drill_groups', 'difficulty',
                    existing_type=sa.Integer(),
                    nullable=False,
                    server_default=sa.text('1'))


def downgrade():
    op.drop_column('drill_groups', 'tags')
    op.drop_column('drill_groups', 'difficulty')
