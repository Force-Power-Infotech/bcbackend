from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context


# Import our synchronous connection setup (before any other imports)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
import use_sync_connection

# This is the Alembic Config object.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add model MetaData objects here for autogenerate support
from app.db.base import Base
from app.db.models.user import User
from app.db.models.session import Session
from app.db.models.shot import Shot
from app.db.models.drill import Drill
from app.db.models.challenge import Challenge

target_metadata = Base.metadata

# Import settings from app
from app.core.config import settings

# Override with sqlalchemy.url from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    url = config.get_main_option("sqlalchemy.url")
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
