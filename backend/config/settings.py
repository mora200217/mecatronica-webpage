import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: list[str]) -> list[str]:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-solo-para-desarrollo-local"
)
DEBUG = env_flag("DJANGO_DEBUG", True)
ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS", ["localhost", "127.0.0.1", "backend", "[::1]"]
)
# En Hetzner, si aún no tienes dominio, pon DJANGO_ALLOWED_HOSTS=*
# para que la API no responda 400 por la IP pública.
if "*" in ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "config.wsgi.application"

# Con POSTGRES_HOST definido usa el contenedor de Postgres; si no, SQLite local.
if os.environ.get("POSTGRES_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "mecatronica").strip(),
            "USER": os.environ.get("POSTGRES_USER", "mecatronica").strip(),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "").strip(),
            "HOST": os.environ["POSTGRES_HOST"].strip(),
            "PORT": os.environ.get("POSTGRES_PORT", "5432").strip(),
            "CONN_MAX_AGE": 60,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Imágenes subidas desde el admin. En Docker esta carpeta es un volumen que
# nginx también monta, para servirlas sin pasar por Django.
MEDIA_URL = "/uploads/"
MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", BASE_DIR / "mediafiles"))
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", BASE_DIR / "content"))

CORS_ALLOWED_ORIGINS = env_list(
    "DJANGO_CORS_ORIGINS",
    ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8080"],
)
if "*" in CORS_ALLOWED_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = []

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", [])
if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = list(CORS_ALLOWED_ORIGINS)
    for host in ALLOWED_HOSTS:
        if host in {"*", "backend"}:
            continue
        CSRF_TRUSTED_ORIGINS.extend([f"http://{host}", f"https://{host}"])
    CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS))

# El botón "Ver el sitio" del admin. En local apunta a Vite; en el servidor a /.
SITE_URL = os.environ.get("PUBLIC_SITE_URL", "/")

# Detrás de nginx / Caddy el esquema real llega en esta cabecera.
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Por defecto las cookies funcionan en HTTP (la IP de Hetzner).
# Cuando tengas HTTPS, pon DJANGO_SECURE_COOKIES=true.
if not DEBUG:
    SESSION_COOKIE_SECURE = env_flag("DJANGO_SECURE_COOKIES", False)
    CSRF_COOKIE_SECURE = env_flag("DJANGO_SECURE_COOKIES", False)
    SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))

# Próximo paso: reemplazar JSON por tablas en Supabase.
SUPABASE_READY = False
