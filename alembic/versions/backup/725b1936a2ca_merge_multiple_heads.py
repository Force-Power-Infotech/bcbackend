"""merge_multiple_heads

Revision ID: 725b1936a2ca
Revises: 02_add_drill_groups, 3c85751f256d, 2023_add_drill_groups, add_drill_type_duration, drill_groups_user_id_nullable
Create Date: 2025-06-03 07:49:02.348358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '725b1936a2ca'
down_revision = ('02_add_drill_groups', '3c85751f256d', '2023_add_drill_groups', 'add_drill_type_duration', 'drill_groups_user_id_nullable')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
