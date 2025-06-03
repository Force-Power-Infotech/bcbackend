"""add phone columns fix

Revision ID: add_phone_columns_fix
Revises: d6a85f3e21f2
Create Date: 2025-06-03 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_phone_columns_fix'
down_revision = 'd6a85f3e21f2'
branch_labels = None
depends_on = None


def upgrade():
    # Add phone number and verification columns
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('phone_verified', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('otp', sa.String(), nullable=True))
    
    # Create index on phone number
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=True)


def downgrade():
    # Drop phone number related columns
    op.drop_index(op.f('ix_users_phone_number'), table_name='users')
    op.drop_column('users', 'otp')
    op.drop_column('users', 'email_verified')
    op.drop_column('users', 'phone_verified')
    op.drop_column('users', 'phone_number')
