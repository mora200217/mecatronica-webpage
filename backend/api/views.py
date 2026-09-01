import json
from pathlib import Path

from django.conf import settings
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

CONTENT_DIR = Path(settings.CONTENT_DIR)


def _load(name: str):
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
            "mode": "json-cms",
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
            ],
        }
    )


@require_GET
def site(request):
    return _ok(_load("site.json"))


@require_GET
def news(request):
    posts = _load("news.json")
    slug = request.GET.get("slug")
    if slug:
        match = next((item for item in posts if item["slug"] == slug), None)
        if not match:
            return HttpResponseNotFound("Noticia no encontrada")
        return _ok(match)
    return _ok(posts)


@require_GET
def events(request):
    return _ok(_load("events.json"))


@require_GET
def history(request):
    return _ok(_load("history.json"))


@require_GET
def industry(request):
    return _ok(_load("industry.json"))


@require_GET
def alumni(request):
    return _ok(_load("alumni.json"))


@require_GET
def program(request):
    return _ok(_load("program.json"))


@require_GET
def jobs(request):
    return _ok(_load("jobs.json"))


@require_GET
def theses(request):
    return _ok(_load("theses.json"))


@require_GET
def curriculum(request):
    return _ok(_load("curriculum.json"))


@require_GET
def redirects(request):
    return _ok(_load("redirects.json"))


@require_GET
def go(request, slug: str):
    items = _load("redirects.json")
    target = next((item for item in items if item["slug"] == slug), None)
    if not target:
        return HttpResponseNotFound("Puente no encontrado")
    return redirect(target["url"])
