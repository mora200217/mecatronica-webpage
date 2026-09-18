COMPOSE_PROD := docker compose -f docker-compose.yml -f docker-compose.prod.yml

.PHONY: help up down logs build restart shell dbshell migrate superuser prod prod-tls prod-down prod-logs prod-update clean

help:
	@echo "Desarrollo local"
	@echo "  make up          Levanta db + backend + frontend con hot reload"
	@echo "  make down        Apaga todo"
	@echo "  make logs        Sigue los logs"
	@echo "  make build       Reconstruye las imágenes"
	@echo "  make shell       Consola dentro del backend"
	@echo "  make dbshell     Consola de Postgres"
	@echo "  make migrate     Aplica migraciones"
	@echo "  make superuser   Crea un usuario del admin de Django"
	@echo "  make reseed      Reimporta el contenido desde content/*.json (pisa lo editado)"
	@echo ""
	@echo "Servidor (Hetzner)"
	@echo "  make prod        Levanta producción con HTTPS (Caddy + Let's Encrypt)"
	@echo "  make prod-update Trae cambios de git, reconstruye y reinicia"
	@echo "  make prod-logs   Logs de producción"
	@echo "  make prod-down   Apaga producción"

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build --no-cache

restart:
	docker compose restart

shell:
	docker compose exec backend sh

dbshell:
	docker compose exec db psql -U $${POSTGRES_USER:-mecatronica} -d $${POSTGRES_DB:-mecatronica}

migrate:
	docker compose exec backend python manage.py migrate

superuser:
	docker compose exec backend python manage.py createsuperuser

reseed:
	docker compose exec backend python manage.py seed_content --force

prod:
	$(COMPOSE_PROD) up -d --build

prod-tls: prod

prod-down:
	$(COMPOSE_PROD) down

prod-logs:
	$(COMPOSE_PROD) logs -f

prod-update:
	git pull --ff-only
	$(COMPOSE_PROD) up -d --build
	$(COMPOSE_PROD) ps

clean:
	docker compose down -v
