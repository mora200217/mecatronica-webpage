#!/bin/sh
set -e

if [ -n "$POSTGRES_HOST" ]; then
  echo "Esperando a Postgres en $POSTGRES_HOST:${POSTGRES_PORT:-5432}..."
  attempt=0
  until python -c "
import os, socket, sys
host = os.environ['POSTGRES_HOST']
port = int(os.environ.get('POSTGRES_PORT', '5432'))
sock = socket.socket()
sock.settimeout(2)
try:
    sock.connect((host, port))
except OSError:
    sys.exit(1)
finally:
    sock.close()
"; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 60 ]; then
      echo "Postgres no respondió a tiempo." >&2
      exit 1
    fi
    sleep 1
  done
  echo "Postgres listo."
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_content
python manage.py ensure_superuser

exec "$@"
