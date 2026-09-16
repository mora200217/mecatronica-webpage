from django.urls import path

from . import views

urlpatterns = [
    path("api/", views.catalog),
    path("api/health", views.health),
    path("api/site", views.site),
    path("api/anniversary", views.anniversary),
    path("api/news", views.news),
    path("api/events", views.events),
    path("api/history", views.history),
    path("api/industry", views.industry),
    path("api/alumni", views.alumni),
    path("api/program", views.program),
    path("api/jobs", views.jobs),
    path("api/theses", views.theses),
    path("api/curriculum", views.curriculum),
    path("api/redirects", views.redirects),
    path("go/<slug:slug>/", views.go, name="go"),
]
