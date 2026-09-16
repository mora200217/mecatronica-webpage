#!/bin/sh
set -e

MEDIA_DIR="${MEDIA_ROOT:-/app/mediafiles}"
mkdir -p "$MEDIA_DIR" /app/staticfiles

# El volumen de fotos llega como root. Ajustamos dueño y bajamos a `app`.
if [ "$(id -u)" = "0" ]; then
  chown -R app:app "$MEDIA_DIR" /app/staticfiles
  exec gosu app /bin/sh "$0" "$@"
fi

if [ -n "$POSTGRES_HOST" ]; then
  echo "Esperando a Postgres en $POSTGRES_HOST:${POSTGRES_PORT:-5432}..."
  python - <<'PY'
import os
import sys
import time

import psycopg

host = os.environ["POSTGRES_HOST"]
port = os.environ.get("POSTGRES_PORT", "5432")
dbname = os.environ.get("POSTGRES_DB", "mecatronica")
user = os.environ.get("POSTGRES_USER", "mecatronica")
password = os.environ.get("POSTGRES_PASSWORD", "").strip()

last = ""
for attempt in range(1, 61):
    try:
        with psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=3,
        ):
            pass
        print("Postgres listo.")
        raise SystemExit(0)
    except psycopg.OperationalError as exc:
        last = str(exc).strip()
        lower = last.lower()
        fatal = (
            "password authentication failed" in lower
            or ("role" in lower and "does not exist" in lower)
        )
        if fatal:
            print("No se pudo entrar a Postgres con el usuario/clave de .env.", file=sys.stderr)
            print(last, file=sys.stderr)
            print(
                "Si cambiaste POSTGRES_PASSWORD o POSTGRES_USER después del "
                "primer arranque, el volumen db-data sigue con los valores viejos. "
                "Restaura la clave original en .env y vuelve a levantar. "
                "Solo si puedes borrar la base: "
                "docker compose -f docker-compose.yml -f docker-compose.prod.yml down -v",
                file=sys.stderr,
            )
            raise SystemExit(1)
        print(f"Esperando a Postgres ({attempt}/60)...")
        time.sleep(1)

print("Postgres no respondió a tiempo.", file=sys.stderr)
if last:
    print(last, file=sys.stderr)
raise SystemExit(1)
PY
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if ! python manage.py seed_content; then
  echo "Aviso: no se pudo sembrar el contenido inicial. El sitio igual arranca." >&2
fi

if ! python manage.py ensure_superuser; then
  echo "Aviso: no se pudo crear el usuario del admin. El sitio igual arranca." >&2
fi

exec "$@"
