#!/bin/sh
# wait-for-it.sh

set -e

hostport="$1"
shift
# Check if the next argument is "--", which is used as a separator
if [ "$1" = "--" ]; then
    shift # Remove the "--" separator
fi
cmd="$@"

# Extract host and port from hostport parameter
host=$(echo $hostport | cut -d: -f1)
port=$(echo $hostport | cut -d: -f2)

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
if [ -n "$cmd" ]; then
    exec $cmd
else
    echo "No command provided to execute after database is available"
fi
