"""create practice_sessions table

Revision ID: create_practice_sessions_table
Revises: add_session_id_to_drills
Create Date: 2025-07-28

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_practice_sessions_table'
down_revision = 'add_session_id_to_drills'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'practice_sessions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('drill_group_id', sa.Integer(), sa.ForeignKey('drill_groups.id', ondelete='CASCADE'), nullable=False),
        sa.Column('drill_id', sa.Integer(), sa.ForeignKey('drills.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index('idx_practice_sessions_user_id', 'practice_sessions', ['user_id'])
    op.create_index('idx_practice_sessions_drill_group_id', 'practice_sessions', ['drill_group_id'])
    op.create_index('idx_practice_sessions_drill_id', 'practice_sessions', ['drill_id'])

def downgrade():
    op.drop_index('idx_practice_sessions_user_id', table_name='practice_sessions')
    op.drop_index('idx_practice_sessions_drill_group_id', table_name='practice_sessions')
    op.drop_index('idx_practice_sessions_drill_id', table_name='practice_sessions')
    op.drop_table('practice_sessions')
