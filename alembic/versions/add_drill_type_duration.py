"""Add new drill fields

Revision ID: add_drill_type_duration
Revises: ccb56bbe21f1
Create Date: 2025-06-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_drill_type_duration'
down_revision = 'ccb56bbe21f1'
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns with nullable=True first
    op.add_column('drills', sa.Column('drill_type', sa.String(), nullable=True))
    op.add_column('drills', sa.Column('duration_minutes', sa.Integer(), nullable=True))
    
    # Update existing records with default values
    op.execute("UPDATE drills SET drill_type = 'DRAW' WHERE drill_type IS NULL")
    op.execute("UPDATE drills SET duration_minutes = 30 WHERE duration_minutes IS NULL")
    
    # Then make them non-nullable
    op.alter_column('drills', 'drill_type',
                    existing_type=sa.String(),
                    nullable=False)
    op.alter_column('drills', 'duration_minutes',
                    existing_type=sa.Integer(),
                    nullable=False)
    
    # Make description non-nullable with default value
    op.execute("UPDATE drills SET description = name WHERE description IS NULL")
    op.alter_column('drills', 'description',
                    existing_type=sa.Text(),
                    nullable=False)
    
    # Make session_id nullable
    op.alter_column('drills', 'session_id',
                    existing_type=sa.Integer(),
                    nullable=True)

def downgrade():
    # Revert session_id to non-nullable
    op.alter_column('drills', 'session_id',
                    existing_type=sa.Integer(),
                    nullable=False)
    
    # Make description nullable again
    op.alter_column('drills', 'description',
                    existing_type=sa.Text(),
                    nullable=True)
    
    # Drop new columns
    op.drop_column('drills', 'duration_minutes')
    op.drop_column('drills', 'drill_type')
