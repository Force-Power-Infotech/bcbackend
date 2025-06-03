"""add_phone_number_and_verification_columns

Revision ID: ccb56bbe21f1
Revises: 01_initial_migration
Create Date: 2025-05-29 16:35:13.805160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccb56bbe21f1'
down_revision = '01_initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    # Migration was completed manually via SQL
    # The following columns were added to the users table:
    # - phone_number VARCHAR(20) NOT NULL with unique index
    # - phone_verified BOOLEAN NOT NULL DEFAULT FALSE
    # - email_verified BOOLEAN NOT NULL DEFAULT FALSE
    pass


def downgrade():
    # If needed, columns can be dropped with:
    # ALTER TABLE users DROP COLUMN email_verified;
    # ALTER TABLE users DROP COLUMN phone_verified;
    # DROP INDEX ix_users_phone_number;
    # ALTER TABLE users DROP COLUMN phone_number;
    pass
