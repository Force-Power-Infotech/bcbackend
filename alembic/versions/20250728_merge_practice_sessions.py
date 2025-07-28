"""merge practice sessions branch

Revision ID: 5b8e2f4d1c3a
Revises: create_practice_sessions_table
Create Date: 2025-07-28

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic
revision: str = '5b8e2f4d1c3a'
down_revision: str = 'create_practice_sessions_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
