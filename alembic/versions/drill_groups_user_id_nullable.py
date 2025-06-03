"""drill_groups_user_id_nullable

Revision ID: drill_groups_user_id_nullable
Revises: make_drill_group_user_id_nullable
Create Date: 2025-06-03 13:17:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'drill_groups_user_id_nullable'
down_revision: Union[str, None] = 'make_drill_group_user_id_nullable'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('drill_groups', 'user_id',
                   existing_type=sa.Integer(),
                   nullable=True)


def downgrade() -> None:
    op.alter_column('drill_groups', 'user_id',
                   existing_type=sa.Integer(),
                   nullable=False)
