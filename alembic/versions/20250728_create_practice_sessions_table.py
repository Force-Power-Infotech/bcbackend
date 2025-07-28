"""create practice_sessions table

Revision ID: 4a7f2d3e9c1b
Revises: 
Create Date: 2025-07-28

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic
revision: str = '4a7f2d3e9c1b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'practice_sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('drill_group_id', sa.Integer(), sa.ForeignKey('drill_groups.id', ondelete='CASCADE'), nullable=False),
        sa.Column('drill_id', sa.Integer(), sa.ForeignKey('drills.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_practice_sessions_user_id', 'practice_sessions', ['user_id'])
    op.create_index('idx_practice_sessions_drill_group_id', 'practice_sessions', ['drill_group_id'])
    op.create_index('idx_practice_sessions_drill_id', 'practice_sessions', ['drill_id'])

def downgrade():
    op.drop_index('idx_practice_sessions_user_id', table_name='practice_sessions')
    op.drop_index('idx_practice_sessions_drill_group_id', table_name='practice_sessions')
    op.drop_index('idx_practice_sessions_drill_id', table_name='practice_sessions')
    op.drop_table('practice_sessions')
