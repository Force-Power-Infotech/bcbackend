"""make drill group user id nullable

Revision ID: make_drill_group_user_id_nullable
Revises: ccb56bbe21f1
Create Date: 2025-06-03 12:47:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'make_drill_group_user_id_nullable'
down_revision: Union[str, None] = 'ccb56bbe21f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make user_id nullable
    op.alter_column('drill_groups', 'user_id',
                    existing_type=sa.Integer(),
                    nullable=True)


def downgrade() -> None:
    # Make user_id non-nullable again
    op.alter_column('drill_groups', 'user_id',
                    existing_type=sa.Integer(),
                    nullable=False)
