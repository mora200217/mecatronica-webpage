import json
from pathlib import Path

from django.conf import settings
from django.db import connection
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from . import serializers
from .models import NewsPost, Redirect

CONTENT_DIR = Path(settings.CONTENT_DIR)


def _load(name: str):
    """Solo queda para la malla, que se genera con un script aparte."""
    path = CONTENT_DIR / name
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _ok(payload):
    response = JsonResponse(payload, safe=False, json_dumps_params={"ensure_ascii": False})
    response["Cache-Control"] = "no-store"
    return response


@require_GET
def catalog(request):
    return _ok(
        {
            "service": "mecatronica-unal-api",
            "mode": "django-cms",
            "supabase": settings.SUPABASE_READY,
            "resources": [
                "/api/site",
                "/api/news",
                "/api/events",
                "/api/history",
                "/api/industry",
                "/api/alumni",
                "/api/program",
                "/api/jobs",
                "/api/theses",
                "/api/curriculum",
                "/api/redirects",
                "/api/anniversary",
                "/api/health",
            ],
        }
    )


@require_GET
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        database = "ok"
    except Exception as exc:  # la usa el healthcheck de Docker
        return JsonResponse({"status": "degraded", "database": str(exc)}, status=503)
    return JsonResponse({"status": "ok", "database": database})


@require_GET
def site(request):
    return _ok(serializers.site_payload())


@require_GET
def news(request):
    slug = request.GET.get("slug")
    if slug:
        post = NewsPost.objects.filter(slug=slug, published=True).first()
        if not post:
            return HttpResponseNotFound("Noticia no encontrada")
        return _ok(serializers.news_item(post))
    return _ok(serializers.news_payload())


@require_GET
def events(request):
    return _ok(serializers.events_payload())


@require_GET
def history(request):
    return _ok(serializers.history_payload())


@require_GET
def anniversary(request):
    return _ok(serializers.anniversary_payload())


@require_GET
def industry(request):
    return _ok(serializers.industry_payload())


@require_GET
def alumni(request):
    return _ok(serializers.alumni_payload())


@require_GET
def program(request):
    return _ok(serializers.program_payload())


@require_GET
def jobs(request):
    return _ok(serializers.jobs_payload())


@require_GET
def theses(request):
    return _ok(serializers.theses_payload())


@require_GET
def curriculum(request):
    # La malla se genera con backend/content/_build_curriculum.py, no se edita en el admin.
    return _ok(_load("curriculum.json"))


@require_GET
def redirects(request):
    return _ok(serializers.redirects_payload())


@require_GET
def go(request, slug: str):
    target = Redirect.objects.filter(slug=slug).first()
    if not target:
        return HttpResponseNotFound("Puente no encontrado")
    return redirect(target.url)
