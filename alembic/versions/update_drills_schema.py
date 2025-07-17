"""Update drills schema

Revision ID: update_drills_schema
Revises: create_drills_table
Create Date: 2025-06-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'update_drills_schema'
down_revision = 'create_drills_table'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing columns to drills table
    op.add_column('drills', sa.Column('session_id', sa.Integer(), nullable=True))
    op.add_column('drills', sa.Column('target_score', sa.Integer(), nullable=True))
    op.add_column('drills', sa.Column('drill_type', sa.String(length=50), nullable=True))
    op.add_column('drills', sa.Column('duration_minutes', sa.Integer(), nullable=True))

    # Add foreign key for session_id if needed
    # Commenting out for now as we don't have the sessions table yet
    # op.create_foreign_key('fk_drills_session_id', 'drills', 'sessions', ['session_id'], ['id'])


def downgrade():
    # Drop the columns in reverse order
    op.drop_column('drills', 'duration_minutes')
    op.drop_column('drills', 'drill_type')
    op.drop_column('drills', 'target_score')
    op.drop_column('drills', 'session_id')
