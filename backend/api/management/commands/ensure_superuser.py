"""Crea un superusuario desde el entorno, si todavía no existe."""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea el usuario del admin si DJANGO_SUPERUSER_USERNAME está definido."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@localhost").strip()

        if not username or not password:
            return

        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            self.stdout.write(f"El usuario {username} ya existe.")
            return

        try:
            user_model.objects.create_superuser(
                username=username, email=email, password=password
            )
        except Exception as exc:
            self.stderr.write(f"No se pudo crear el usuario {username}: {exc}")
            return
        self.stdout.write(self.style.SUCCESS(f"Usuario del admin creado: {username}"))
