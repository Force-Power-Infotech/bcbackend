#!/bin/bash
set -e

# Function to check if database exists
database_exists() {
    psql -U "$POSTGRES_USER" -lqt | cut -d \| -f 1 | grep -qw "$POSTGRES_DB"
}

# Create database if it doesn't exist
if ! database_exists; then
    echo "Creating database: $POSTGRES_DB"
    createdb -U "$POSTGRES_USER" "$POSTGRES_DB"
fi

# Connect to the database
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
    -- Create extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    -- Set timezone
    SET timezone = 'UTC';

    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS public;

    -- Grant privileges
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "$POSTGRES_USER";
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "$POSTGRES_USER";
EOSQL
