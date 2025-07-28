"""alter alembic version column size

Revision ID: a1
Create Date: 2025-06-03 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create alembic_version table with longer version_num column
    op.execute('DROP TABLE IF EXISTS alembic_version')
    op.create_table(
        'alembic_version',
        sa.Column('version_num', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('version_num')
    )
    
    # Create initial tables
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('phone_verified', sa.Boolean(), nullable=True),
        sa.Column('email_verified', sa.Boolean(), nullable=True),
        sa.Column('otp', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_phone_number', 'users', ['phone_number'], unique=True)


def downgrade():
    op.drop_table('alembic_version')
    op.drop_table('users')
