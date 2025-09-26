#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for MySQL..."

for i in {1..60}; do
  if nc -z mysql 3306; then
    echo "MySQL is ready"

    # Якщо немає жодної міграції — створимо
    if [ -z "$(ls -A alembic/versions 2>/dev/null)" ]; then
      echo "[entrypoint] No migrations found. Creating initial..."
      alembic revision --autogenerate -m "init schema"
    fi

    exec "$@"
  fi
  sleep 2
done

echo "ERROR: MySQL did not become ready in time (120s)" >&2
exit 1