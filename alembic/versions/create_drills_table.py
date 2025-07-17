"""Create drills table

Revision ID: create_drills_table
Revises: add_drill_group_columns
Create Date: 2025-06-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_drills_table'
down_revision = 'add_drill_group_columns'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'drills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('difficulty', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_drills_name'), 'drills', ['name'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_drills_name'), table_name='drills')
    op.drop_table('drills')
