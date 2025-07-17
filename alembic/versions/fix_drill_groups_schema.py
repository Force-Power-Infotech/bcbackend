"""Fix drill_groups table schema

Revision ID: fix_drill_groups_schema
Revises: fix_drill_group_drills
Create Date: 2025-06-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fix_drill_groups_schema'
down_revision = 'fix_drill_group_drills'
branch_labels = None
depends_on = None


def upgrade():
    # Drop existing foreign key
    op.drop_constraint('drill_groups_user_id_fkey', 'drill_groups', type_='foreignkey')

    # Update null values first
    op.execute("UPDATE drill_groups SET updated_at = created_at WHERE updated_at IS NULL")
    op.execute("UPDATE drill_groups SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
    op.execute("UPDATE drill_groups SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
    op.execute("UPDATE drill_groups SET user_id = (SELECT id FROM users LIMIT 1) WHERE user_id IS NULL")
    
    # Update column types
    op.alter_column('drill_groups',
        'name',
        existing_type=sa.VARCHAR(),
        type_=sa.String(255),
        existing_nullable=False)
    op.alter_column('drill_groups',
        'description',
        existing_type=sa.VARCHAR(),
        type_=sa.Text(),
        existing_nullable=True)
    op.alter_column('drill_groups',
        'user_id',
        existing_type=sa.INTEGER(),
        nullable=False)
    
    # Update timestamp columns
    op.execute("ALTER TABLE drill_groups ALTER COLUMN created_at TYPE timestamp without time zone")
    op.execute("ALTER TABLE drill_groups ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP")
    op.execute("ALTER TABLE drill_groups ALTER COLUMN created_at SET NOT NULL")
    
    op.execute("ALTER TABLE drill_groups ALTER COLUMN updated_at TYPE timestamp without time zone")
    op.execute("ALTER TABLE drill_groups ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP")
    op.execute("ALTER TABLE drill_groups ALTER COLUMN updated_at SET NOT NULL")
    
    # Add back foreign key with CASCADE
    op.create_foreign_key(
        'drill_groups_user_id_fkey',
        'drill_groups', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    # Drop foreign key
    op.drop_constraint('drill_groups_user_id_fkey', 'drill_groups', type_='foreignkey')

    # Revert column changes
    op.alter_column('drill_groups',
        'name',
        existing_type=sa.String(255),
        type_=sa.VARCHAR(),
        existing_nullable=False)
    op.alter_column('drill_groups',
        'description',
        existing_type=sa.Text(),
        type_=sa.VARCHAR(),
        existing_nullable=True)
    op.alter_column('drill_groups',
        'user_id',
        existing_type=sa.INTEGER(),
        nullable=True)
    op.alter_column('drill_groups',
        'created_at',
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        nullable=True,
        server_default=sa.text('now()'))
    op.alter_column('drill_groups',
        'updated_at',
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        nullable=True,
        server_default=None)

    # Add back original foreign key
    op.create_foreign_key(
        'drill_groups_user_id_fkey',
        'drill_groups', 'users',
        ['user_id'], ['id']
    )
