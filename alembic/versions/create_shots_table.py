"""Create shots table

Revision ID: create_shots_table
Revises: add_session_id_fkey
Create Date: 2025-06-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_shots_table'
down_revision = 'add_session_id_fkey'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'shots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('drill_id', sa.Integer(), nullable=True),
        sa.Column('shot_type', sa.Enum('draw', 'drive', 'weighted', name='shottype'), nullable=False),
        sa.Column('distance_meters', sa.Float(), nullable=True),
        sa.Column('accuracy_score', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['drill_id'], ['drills.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shots_drill_id'), 'shots', ['drill_id'], unique=False)
    op.create_index(op.f('ix_shots_session_id'), 'shots', ['session_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_shots_session_id'), table_name='shots')
    op.drop_index(op.f('ix_shots_drill_id'), table_name='shots')
    op.drop_table('shots')
    op.execute('DROP TYPE shottype')
