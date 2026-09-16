# Ingeniería Mecatrónica UNAL — sitio MVP

Sitio de la carrera (Pumpleaños 25) pensado para quedarse: estudiantes, egresados y la siguiente generación que lo va a editar.

## Qué hay

| Capa | Rol |
| --- | --- |
| `frontend/` | React + Vite. Pestañas, malla, noticias, historia interactiva. |
| `backend/` | Django. API + panel de administración (CMS) en `/admin/`. |
| `db` | PostgreSQL 16 en contenedor. |
| `backend/content/*.json` | Semilla inicial: se importa una vez a la base. Después se edita en el admin. |
| Fotos | Wikimedia Commons, campus y Facultad de Ingeniería, en `frontend/public/media/`. |

## Correrlo en local (Docker)

Necesitas Docker Desktop. Todo lo demás lo pone el contenedor.

```bash
cp .env.example .env     # la primera vez
make up                  # o: docker compose up --build
```

| URL | Qué es |
| --- | --- |
| http://localhost:5173 | La web (Vite con hot reload) |
| http://localhost:8000/api/ | La API de Django |
| http://localhost:8000/admin/ | Panel para editar el contenido |
| localhost:5433 | Postgres, por si te quieres conectar con un cliente |

Guardas un archivo y se recarga solo: el código de `backend/` y `frontend/` está montado dentro de los contenedores.

Comandos útiles: `make logs`, `make shell`, `make dbshell`, `make superuser`, `make down`.
`make clean` apaga todo y **borra la base de datos**.

### Sin Docker

```bash
cd backend && python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && python manage.py migrate && python manage.py runserver 8000

cd frontend && npm install && npm run dev
```

Sin `POSTGRES_HOST` en el entorno, Django usa SQLite. Vite reenvía `/api` y `/go` a Django.

## Desplegar en Hetzner (Ubuntu)

Hace falta un servidor Ubuntu (Cloud o Robot), con los puertos **22, 80 y 443** abiertos en el firewall de Hetzner. El código de Docker tiene que estar en GitHub: si aún no lo has subido, haz commit y `git push` desde esta máquina.

### 1. Entra al servidor

```bash
ssh root@IP_DEL_SERVIDOR
```

### 2. Instala Docker (una sola vez)

```bash
curl -fsSL https://get.docker.com | sh
apt update && apt install -y git make ufw
ufw allow OpenSSH
ufw allow 80
ufw allow 443
ufw --force enable
```

### 3. Trae el repo

```bash
git clone https://github.com/mora200217/mecatronica-webpage.git /opt/mecatronica
cd /opt/mecatronica
cp .env.example .env
nano .env
```

Cambia **todas** las contraseñas. Genera la de Django con:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

Si de momento solo tienes la IP (por ejemplo `168.119.x.x`):

```
POSTGRES_PASSWORD=...clave larga...
DJANGO_SECRET_KEY=...la que generaste...
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=*
DJANGO_CORS_ORIGINS=*
DJANGO_CSRF_TRUSTED_ORIGINS=http://168.119.x.x
DJANGO_SECURE_COOKIES=false
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=...otra clave larga...
DJANGO_SUPERUSER_EMAIL=tu@correo
WEB_PORT=80
```

### 4. Arranca el sitio

```bash
make prod
```

Eso construye las imágenes y deja nginx escuchando en el puerto 80. En el navegador: `http://IP_DEL_SERVIDOR`. El panel: `http://IP_DEL_SERVIDOR/admin/`. La API: `http://IP_DEL_SERVIDOR/api/health`.

No abras el puerto 8000. Nginx habla con Django por la red interna de Docker.

Para ver si levantó: `make prod-logs`. Para actualizar después de un `git push`: `cd /opt/mecatronica && make prod-update`.

### 5. HTTPS cuando tengas dominio

En el DNS del dominio crea un registro **A** hacia la IP del servidor. Espera a que resuelva (`ping tudominio.co`). En `.env`:

```
WEB_PORT=8080
SITE_DOMAIN=tudominio.co
DJANGO_ALLOWED_HOSTS=tudominio.co,www.tudominio.co,backend
DJANGO_CORS_ORIGINS=https://tudominio.co,https://www.tudominio.co
DJANGO_CSRF_TRUSTED_ORIGINS=https://tudominio.co,https://www.tudominio.co
```

```bash
make prod-tls
```

Caddy pide el certificado a Let's Encrypt y lo renueva solo. El sitio queda en `https://tudominio.co`.

### Cómo están armados los contenedores

- **db**: `postgres:16-alpine`, datos en el volumen `db-data`. No se expone al exterior en producción.
- **backend**: Django con gunicorn. Al arrancar espera a Postgres, corre `migrate` y `collectstatic`. Los estáticos del admin los sirve WhiteNoise. Tiene healthcheck en `/api/health`.
- **frontend**: build de Vite servido por nginx, que además hace de proxy de `/api`, `/go`, `/admin` y `/static` hacia el backend. Por eso todo sale por un solo puerto.

`docker-compose.yml` es la base, `docker-compose.override.yml` es desarrollo (Compose lo aplica solo) y `docker-compose.prod.yml` es el servidor.

## Cómo editar el contenido

Casi todo se edita en el panel: [http://localhost:8000/admin/](http://localhost:8000/admin/).

En local: `make superuser` (o `docker compose exec backend python manage.py changepassword admin` si el usuario ya existe). En el servidor pon una clave larga en `.env` (`DJANGO_SUPERUSER_*`) antes del primer arranque.

Ahí están noticias, egresados, industria, programa, ofertas, tesis, historia, el carrusel y la programación del aniversario.

**La excepción es la malla curricular.** Sigue en `backend/content/curriculum.json` y se regenera con `python backend/content/_build_curriculum.py`. El PDF oficial está en Puentes → *Malla curricular*.

Los JSON de `backend/content/` son solo la semilla. Si quieres volver al contenido original: `make reseed` (pisa lo que hayas editado en el admin).

## Orquestador

`GET /go/sia/` redirige a SIA. Lo mismo para correo, Hermes, PEP, malla PDF, etc. La UI está en `/puentes`.

## Qué sigue (Supabase)

Cada modelo del admin es una tabla. Django puede seguir siendo el orquestador y, más adelante, leer de Supabase. No hay que rehacer las pantallas.

## Créditos de fotos

Imágenes de [Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:Edificio_de_Ingenier%C3%ADa_-_Universidad_Nacional_de_Colombia,_Bogot%C3%A1) (Facultad de Ingeniería, Edificio CyT, aulas).

El logo de los 25 años sale del material de la Facultad de Ingeniería. Este sitio es la casa de la celebración.
