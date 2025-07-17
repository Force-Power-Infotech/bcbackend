#!/bin/bash
set -e

# Wait for database
echo "Waiting for database..."
wait-for-it.sh db:5432 -t 60

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Create default user
echo "Creating default user..."
python scripts/create_default_user.py

# Verify default user was created
echo "Verifying default user..."
PGPASSWORD=postgres psql -h db -U postgres -d bowlsacedb -c "SELECT id, email, username FROM users WHERE id = 1;"

# Start the application
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug
