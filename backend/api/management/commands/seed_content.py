"""Carga los archivos de `content/*.json` en la base de datos.

Se ejecuta solo al arrancar: si ya hay contenido no toca nada, para no
pisar lo que alguien editó desde el admin. Con --force vuelve a importar
todo desde los JSON.
"""

import json
from datetime import date, datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from api import models

CONTENT_DIR = Path(settings.CONTENT_DIR)


def load(name: str):
    path = CONTENT_DIR / name
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_date(value: str) -> date | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_datetime(value: str):
    if not value:
        return None
    parsed = datetime.fromisoformat(value)
    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed)
    return parsed


def join(values) -> str:
    return ", ".join(values or [])


class Command(BaseCommand):
    help = "Importa el contenido inicial desde los archivos JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Borra el contenido actual y lo vuelve a importar desde los JSON.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options["force"]

        if models.NewsPost.objects.exists() and not force:
            self.stdout.write("Ya hay contenido en la base de datos. Nada que hacer.")
            return

        if force:
            self.stdout.write("Borrando contenido actual...")
            for model in (
                models.AgendaSlot,
                models.AnniversaryDay,
                models.AnniversaryHighlight,
                models.GalleryPhoto,
                models.HistoryMilestone,
                models.HistoryEra,
                models.HistoryStat,
                models.Redirect,
                models.Thesis,
                models.Job,
                models.ResearchGroup,
                models.Lab,
                models.FacultyMember,
                models.IndustryPartner,
                models.IndustrySector,
                models.Alumnus,
                models.Event,
                models.EventCategory,
                models.NewsPost,
                models.HeroSlide,
            ):
                model.objects.all().delete()

        self.seed_site()
        self.seed_news()
        self.seed_events()
        self.seed_alumni()
        self.seed_industry()
        self.seed_program()
        self.seed_jobs()
        self.seed_theses()
        self.seed_redirects()
        self.seed_history()
        self.seed_anniversary()
        self.stdout.write(self.style.SUCCESS("Contenido importado."))

    # ---------------------------------------------------------------- site

    def seed_site(self):
        data = load("site.json")
        if not data:
            return
        birthday = data.get("birthday", {})
        contact = data.get("contact", {})
        row = models.SiteSettings.load()
        row.program = data.get("program", "")
        row.faculty = data.get("faculty", "")
        row.university = data.get("university", "")
        row.campus = data.get("campus", "")
        row.snies = data.get("snies", "")
        row.sia = data.get("sia", "")
        row.credits = data.get("credits", 179)
        row.semesters = data.get("semesters", 10)
        row.created = data.get("created", 2001)
        row.title = data.get("title", "")
        row.tagline = data.get("tagline", "")
        row.birthday_years = birthday.get("years", 25)
        row.birthday_kicker = birthday.get("kicker", "")
        row.birthday_headline = birthday.get("headline", "")
        row.birthday_body = birthday.get("body", "")
        row.contact_coordinator = contact.get("coordinator", "")
        row.contact_email = contact.get("email", "")
        row.contact_building = contact.get("building", "")
        row.contact_address = contact.get("address", "")
        row.contact_phone = contact.get("phone", "")
        row.disclaimer = data.get("disclaimer", "")
        row.save()

        for index, slide in enumerate(data.get("hero", [])):
            cta = slide.get("cta", {})
            models.HeroSlide.objects.create(
                order=index,
                image_url=slide.get("image", ""),
                label=slide.get("label", ""),
                kicker=slide.get("kicker", ""),
                title=slide.get("title", ""),
                body=slide.get("body", ""),
                accent=slide.get("accent", False),
                cta_label=cta.get("label", ""),
                cta_to=cta.get("to", ""),
                cta_href=cta.get("href", ""),
            )

    # ---------------------------------------------------------------- news

    def seed_news(self):
        for post in load("news.json") or []:
            models.NewsPost.objects.create(
                slug=post["slug"],
                title=post.get("title", ""),
                kicker=post.get("kicker", ""),
                date=parse_date(post.get("date", "")) or date.today(),
                excerpt=post.get("excerpt", ""),
                body=post.get("body", ""),
                image_url=post.get("image", ""),
            )

    def seed_events(self):
        data = load("events.json") or {}
        categories = {}
        for index, item in enumerate(data.get("filters", [])):
            categories[item["id"]] = models.EventCategory.objects.create(
                slug=item["id"], label=item["label"], order=index
            )
        for index, item in enumerate(data.get("items", [])):
            category = categories.get(item.get("type"))
            if category is None:
                continue
            models.Event.objects.create(
                order=index,
                category=category,
                month=item.get("month", ""),
                day=item.get("day", ""),
                title=item.get("title", ""),
                place=item.get("place", ""),
            )

    # ------------------------------------------------------------- people

    def seed_alumni(self):
        data = load("alumni.json") or {}
        page = models.AlumniPage.load()
        page.note = data.get("note", "")
        page.save()
        for index, person in enumerate(data.get("people", [])):
            models.Alumnus.objects.create(
                order=index,
                name=person.get("name", ""),
                cohort=person.get("cohort", ""),
                role=person.get("role", ""),
                company=person.get("company", ""),
                city=person.get("city", ""),
                focus=person.get("focus", ""),
                linkedin=person.get("linkedin", ""),
                mentorship=person.get("mentorship", False),
            )

    def seed_industry(self):
        data = load("industry.json") or {}
        page = models.IndustryPage.load()
        page.pitch = data.get("pitch", "")
        page.save()
        for index, sector in enumerate(data.get("sectors", [])):
            models.IndustrySector.objects.create(
                order=index,
                name=sector.get("name", ""),
                body=sector.get("body", ""),
                examples=join(sector.get("examples")),
            )
        for index, partner in enumerate(data.get("partners", [])):
            models.IndustryPartner.objects.create(
                order=index, name=partner.get("name", ""), role=partner.get("role", "")
            )

    def seed_program(self):
        data = load("program.json") or {}
        page = models.ProgramPage.load()
        page.about = data.get("about", "")
        page.save()
        for index, person in enumerate(data.get("faculty", [])):
            models.FacultyMember.objects.create(
                order=index,
                name=person.get("name", ""),
                role=person.get("role", ""),
                area=person.get("area", ""),
                email=person.get("email", ""),
                real=person.get("real", False),
            )
        for index, lab in enumerate(data.get("labs", [])):
            models.Lab.objects.create(
                order=index,
                name=lab.get("name", ""),
                building=lab.get("building", ""),
                github=lab.get("github", ""),
                body=lab.get("body", ""),
            )
        for index, group in enumerate(data.get("groups", [])):
            models.ResearchGroup.objects.create(
                order=index,
                name=group.get("name", ""),
                line=group.get("line", ""),
                hermes=group.get("hermes", ""),
            )

    # --------------------------------------------------------------- work

    def seed_jobs(self):
        for index, job in enumerate(load("jobs.json") or []):
            models.Job.objects.create(
                order=index,
                title=job.get("title", ""),
                company=job.get("company", ""),
                type=job.get("type", ""),
                area=job.get("area", ""),
                deadline=parse_date(job.get("deadline", "")),
                body=job.get("body", ""),
            )

    def seed_theses(self):
        for index, thesis in enumerate(load("theses.json") or []):
            models.Thesis.objects.create(
                order=index,
                year=thesis.get("year", 2026),
                title=thesis.get("title", ""),
                authors=thesis.get("authors", ""),
                modality=thesis.get("modality", ""),
                tags=join(thesis.get("tags")),
            )

    def seed_redirects(self):
        for index, item in enumerate(load("redirects.json") or []):
            models.Redirect.objects.create(
                order=index,
                slug=item["slug"],
                title=item.get("title", ""),
                group=item.get("group", ""),
                description=item.get("description", ""),
                url=item.get("url", ""),
            )

    # ------------------------------------------------------------ history

    def seed_history(self):
        data = load("history.json") or {}
        page = models.HistoryPage.load()
        page.intro = data.get("intro", "")
        page.save()

        for index, stat in enumerate(data.get("stats", [])):
            models.HistoryStat.objects.create(
                order=index,
                key=stat["id"],
                value=stat.get("value", 0),
                kind=stat.get("kind", "count"),
                label=stat.get("label", ""),
                detail=stat.get("detail", ""),
            )

        eras = {}
        for index, era in enumerate(data.get("eras", [])):
            eras[era["id"]] = models.HistoryEra.objects.create(
                order=index,
                slug=era["id"],
                label=era.get("label", ""),
                range_label=era.get("range", ""),
            )

        for index, item in enumerate(data.get("timeline", [])):
            era = eras.get(item.get("era"))
            if era is None:
                continue
            figure = item.get("figure", {})
            models.HistoryMilestone.objects.create(
                order=index,
                era=era,
                year=item.get("year", ""),
                title=item.get("title", ""),
                body=item.get("body", ""),
                figure_value=figure.get("value", ""),
                figure_label=figure.get("label", ""),
                tags=join(item.get("tags")),
                image_url=item.get("image", ""),
            )

        for index, photo in enumerate(data.get("gallery", [])):
            models.GalleryPhoto.objects.create(
                order=index,
                title=photo.get("title", ""),
                caption=photo.get("caption", ""),
                credit=photo.get("credit", ""),
                image_url=photo.get("src", ""),
            )

    # -------------------------------------------------------- anniversary

    def seed_anniversary(self):
        data = load("anniversary.json") or {}
        cta = data.get("cta", {})
        contact = data.get("contact", {})
        event = models.AnniversaryEvent.load()
        event.kicker = data.get("kicker", "")
        event.headline = data.get("headline", "")
        event.lead = data.get("lead", "")
        event.years = data.get("years", 25)
        event.logo_url = data.get("logo", "")
        event.logo_ink_url = data.get("logoInk", "")
        event.image_url = data.get("banner", "")
        event.starts_at = parse_datetime(data.get("startsAt", ""))
        event.ends_at = parse_datetime(data.get("endsAt", ""))
        event.date_label = data.get("dateLabel", "")
        event.venue = data.get("venue", "")
        event.cta_label = cta.get("label", "")
        event.cta_to = cta.get("to", "")
        event.contact_email = contact.get("email", "")
        event.contact_phone = contact.get("phone", "")
        event.credit = data.get("credit", "")
        event.save()

        for index, item in enumerate(data.get("highlights", [])):
            models.AnniversaryHighlight.objects.create(
                order=index, key=item["id"], title=item.get("title", ""), body=item.get("body", "")
            )

        for index, day in enumerate(data.get("days", [])):
            row = models.AnniversaryDay.objects.create(
                order=index,
                key=day["id"],
                label=day.get("label", ""),
                date_label=day.get("date", ""),
                theme=day.get("theme", ""),
            )
            for slot_index, slot in enumerate(day.get("agenda", [])):
                models.AgendaSlot.objects.create(
                    day=row,
                    order=slot_index,
                    time=slot.get("time", ""),
                    end=slot.get("end", ""),
                    title=slot.get("title", ""),
                    note=slot.get("note", ""),
                    track=slot.get("track", "acto"),
                )
