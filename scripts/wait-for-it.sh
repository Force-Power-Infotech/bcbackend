#!/bin/sh
# wait-for-it.sh

set -e

host="db"
port="5432"

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - running migrations"

# Clean up any existing alembic migrations
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c 'DROP TABLE IF EXISTS alembic_version;'

# Create initial tables manually since there are multiple alembic heads
echo "Creating users table"
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c '
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    phone_number VARCHAR(255) UNIQUE,
    phone_verified BOOLEAN DEFAULT FALSE,
    email_verified BOOLEAN DEFAULT FALSE,
    otp VARCHAR(255)
);
'

echo "Creating drill_groups table"
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c '
CREATE TABLE IF NOT EXISTS drill_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    difficulty INTEGER DEFAULT 1,
    tags JSONB DEFAULT '\''[]'\'',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    image VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
'

echo "Creating drills table"
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c '
CREATE TABLE IF NOT EXISTS drills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    difficulty INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    session_id INTEGER,
    target_score INTEGER,
    drill_type VARCHAR(50),
    duration_minutes INTEGER
);
'

echo "Creating drill_group_drills table"
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c '
CREATE TABLE IF NOT EXISTS drill_group_drills (
    id SERIAL PRIMARY KEY,
    drill_group_id INTEGER NOT NULL,
    drill_id INTEGER NOT NULL,
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drill_group_id) REFERENCES drill_groups (id),
    FOREIGN KEY (drill_id) REFERENCES drills (id)
);
'

echo "Creating practice_sessions table"
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c '
CREATE TABLE IF NOT EXISTS practice_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    drill_group_id INTEGER NOT NULL,
    drill_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (drill_group_id) REFERENCES drill_groups (id),
    FOREIGN KEY (drill_id) REFERENCES drills (id)
);
CREATE INDEX IF NOT EXISTS idx_practice_sessions_user_id ON practice_sessions (user_id);
CREATE INDEX IF NOT EXISTS idx_practice_sessions_drill_group_id ON practice_sessions (drill_group_id);
CREATE INDEX IF NOT EXISTS idx_practice_sessions_drill_id ON practice_sessions (drill_id);
'

# Create alembic version table to mark migrations as complete
echo "Creating alembic_version table"
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c '
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(128) PRIMARY KEY
);
INSERT INTO alembic_version (version_num) VALUES ('\''a1'\'');
'

>&2 echo "Verifying tables exist"
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c '\dt'

>&2 echo "Creating admin user if it doesn't exist"
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "postgres" -d "bowlsacedb" -c "
INSERT INTO users (email, username, hashed_password, full_name, is_active, is_admin, created_at, updated_at, phone_verified, email_verified)
VALUES ('admin@bowlsace.com', 'admin', '\$2b\$12\$CX0RfHVz7elbqQn.44jEEuJZa9tz4KKVYfAJ5yHo39iWjNBqDzqoi', 'Admin User', true, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, true, true)
ON CONFLICT (email) DO NOTHING;
"

>&2 echo "Starting FastAPI application"
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
