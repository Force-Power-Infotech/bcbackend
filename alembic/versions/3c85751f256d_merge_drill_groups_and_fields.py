"""merge drill groups and fields

Revision ID: 3c85751f256d
Revises: 2023_06_02_drill_fields_merge, d6a85f3e21f2
Create Date: 2025-06-02 11:48:30.286402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c85751f256d'
down_revision = ('2023_06_02_drill_fields_merge', 'd6a85f3e21f2')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
