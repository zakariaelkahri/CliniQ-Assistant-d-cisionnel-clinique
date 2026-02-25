#!/usr/bin/env sh
set -e

# Defaults
: "${UVICORN_HOST:=0.0.0.0}"
: "${UVICORN_PORT:=8000}"
: "${POSTGRES_HOST:=postgres}"
: "${POSTGRES_PORT:=5432}"

# Wait for Postgres
echo "Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
for i in $(seq 1 60); do
    if nc -z "$POSTGRES_HOST" "$POSTGRES_PORT" 2>/dev/null; then
        echo "Postgres is ready!"
        break
    fi
    echo "Attempt $i/60: Postgres not ready yet..."
    sleep 2
done

# Additional verification
if ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT" 2>/dev/null; then
    echo "ERROR: Could not connect to Postgres at $POSTGRES_HOST:$POSTGRES_PORT"
    exit 1
fi

exec uvicorn app.main:app --host "$UVICORN_HOST" --port "$UVICORN_PORT" --reload