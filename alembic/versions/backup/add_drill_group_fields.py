"""Add drill group fields

Revision ID: add_drill_group_fields
Revises: drill_groups_user_id_nullable
Create Date: 2025-06-03 12:00:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = 'add_drill_group_fields'
down_revision: Union[str, None] = 'drill_groups_user_id_nullable'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('drill_groups', sa.Column('is_public', sa.Boolean(), nullable=True, server_default='true'))
    op.add_column('drill_groups', sa.Column('difficulty', sa.Integer(), nullable=True, server_default='1'))
    op.add_column('drill_groups', sa.Column('tags', JSONB(), nullable=True, server_default='[]'))


def downgrade() -> None:
    op.drop_column('drill_groups', 'is_public')
    op.drop_column('drill_groups', 'difficulty')
    op.drop_column('drill_groups', 'tags')
