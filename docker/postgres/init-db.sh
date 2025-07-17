#!/bin/bash
set -e


# Create the database if it does not exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    DO
    $$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRES_DB') THEN
            CREATE DATABASE "$POSTGRES_DB";
        END IF;
    END
    $$;
EOSQL

# Create extension and set up permissions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "$POSTGRES_USER";
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "$POSTGRES_USER";
EOSQL
