"""Arma las respuestas de la API a partir de los modelos.

Las formas de los JSON son las mismas que consumía el frontend cuando el
contenido vivía en `content/*.json`, así que las pantallas no cambian.
"""

from . import models


def _split(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(",") if part.strip()]


def _date(value) -> str:
    return value.isoformat() if value else ""


def site_payload() -> dict:
    settings_row = models.SiteSettings.load()
    return {
        "program": settings_row.program,
        "faculty": settings_row.faculty,
        "university": settings_row.university,
        "campus": settings_row.campus,
        "snies": settings_row.snies,
        "sia": settings_row.sia,
        "credits": settings_row.credits,
        "semesters": settings_row.semesters,
        "created": settings_row.created,
        "title": settings_row.title,
        "birthday": {
            "years": settings_row.birthday_years,
            "headline": settings_row.birthday_headline,
            "kicker": settings_row.birthday_kicker,
            "body": settings_row.birthday_body,
        },
        "hero": [hero_slide(item) for item in models.HeroSlide.objects.all()],
        "tagline": settings_row.tagline,
        "contact": {
            "coordinator": settings_row.contact_coordinator,
            "email": settings_row.contact_email,
            "building": settings_row.contact_building,
            "address": settings_row.contact_address,
            "phone": settings_row.contact_phone,
        },
        "disclaimer": settings_row.disclaimer,
    }


def hero_slide(item: models.HeroSlide) -> dict:
    payload = {
        "image": item.image_src,
        "label": item.label,
        "kicker": item.kicker,
        "title": item.title,
        "body": item.body,
    }
    if item.accent:
        payload["accent"] = True
    if item.cta_label:
        cta = {"label": item.cta_label}
        if item.cta_href:
            cta["href"] = item.cta_href
        else:
            cta["to"] = item.cta_to
        payload["cta"] = cta
    return payload


def news_item(post: models.NewsPost) -> dict:
    return {
        "slug": post.slug,
        "title": post.title,
        "date": _date(post.date),
        "kicker": post.kicker,
        "image": post.image_src,
        "excerpt": post.excerpt,
        "body": post.body,
    }


def news_payload() -> list[dict]:
    return [news_item(post) for post in models.NewsPost.objects.filter(published=True)]


def events_payload() -> dict:
    return {
        "filters": [
            {"id": category.slug, "label": category.label}
            for category in models.EventCategory.objects.all()
        ],
        "items": [
            {
                "id": f"e{event.pk}",
                "month": event.month,
                "day": event.day,
                "title": event.title,
                "place": event.place,
                "type": event.category.slug,
            }
            for event in models.Event.objects.select_related("category")
        ],
    }


def history_payload() -> dict:
    return {
        "intro": models.HistoryPage.load().intro,
        "stats": [
            {
                "id": stat.key,
                "value": stat.value,
                "kind": stat.kind,
                "label": stat.label,
                "detail": stat.detail,
            }
            for stat in models.HistoryStat.objects.all()
        ],
        "eras": [
            {"id": era.slug, "label": era.label, "range": era.range_label}
            for era in models.HistoryEra.objects.all()
        ],
        "timeline": [
            {
                "year": item.year,
                "era": item.era.slug,
                "title": item.title,
                "body": item.body,
                "figure": {"value": item.figure_value, "label": item.figure_label},
                "tags": _split(item.tags),
                "image": item.image_src,
            }
            for item in models.HistoryMilestone.objects.select_related("era")
        ],
        "gallery": [
            {
                "src": photo.image_src,
                "title": photo.title,
                "caption": photo.caption,
                "credit": photo.credit,
            }
            for photo in models.GalleryPhoto.objects.all()
        ],
    }


def industry_payload() -> dict:
    return {
        "pitch": models.IndustryPage.load().pitch,
        "sectors": [
            {"name": sector.name, "body": sector.body, "examples": _split(sector.examples)}
            for sector in models.IndustrySector.objects.all()
        ],
        "partners": [
            {"name": partner.name, "role": partner.role}
            for partner in models.IndustryPartner.objects.all()
        ],
    }


def alumni_payload() -> dict:
    return {
        "note": models.AlumniPage.load().note,
        "people": [
            {
                "name": person.name,
                "cohort": person.cohort,
                "role": person.role,
                "company": person.company,
                "city": person.city,
                "focus": person.focus,
                "mentorship": person.mentorship,
            }
            for person in models.Alumnus.objects.all()
        ],
    }


def program_payload() -> dict:
    return {
        "about": models.ProgramPage.load().about,
        "faculty": [
            {
                "name": person.name,
                "role": person.role,
                "area": person.area,
                "email": person.email,
                "real": person.real,
            }
            for person in models.FacultyMember.objects.all()
        ],
        "labs": [
            {"name": lab.name, "building": lab.building, "github": lab.github, "body": lab.body}
            for lab in models.Lab.objects.all()
        ],
        "groups": [
            {"name": group.name, "line": group.line, "hermes": group.hermes}
            for group in models.ResearchGroup.objects.all()
        ],
    }


def jobs_payload() -> list[dict]:
    return [
        {
            "id": f"job-{job.pk}",
            "title": job.title,
            "company": job.company,
            "type": job.type,
            "area": job.area,
            "deadline": _date(job.deadline),
            "body": job.body,
        }
        for job in models.Job.objects.filter(published=True)
    ]


def theses_payload() -> list[dict]:
    return [
        {
            "year": thesis.year,
            "title": thesis.title,
            "authors": thesis.authors,
            "modality": thesis.modality,
            "tags": _split(thesis.tags),
        }
        for thesis in models.Thesis.objects.all()
    ]


def redirects_payload() -> list[dict]:
    return [
        {
            "slug": item.slug,
            "title": item.title,
            "group": item.group,
            "description": item.description,
            "url": item.url,
        }
        for item in models.Redirect.objects.all()
    ]


def anniversary_payload() -> dict:
    event = models.AnniversaryEvent.load()
    return {
        "kicker": event.kicker,
        "headline": event.headline,
        "lead": event.lead,
        "years": event.years,
        "logo": event.logo_src,
        "logoInk": event.logo_ink_src,
        "banner": event.image_src,
        "startsAt": event.starts_at.isoformat() if event.starts_at else "",
        "endsAt": event.ends_at.isoformat() if event.ends_at else "",
        "dateLabel": event.date_label,
        "venue": event.venue,
        "cta": {"label": event.cta_label, "to": event.cta_to},
        "contact": {"email": event.contact_email, "phone": event.contact_phone},
        "highlights": [
            {"id": item.key, "title": item.title, "body": item.body}
            for item in models.AnniversaryHighlight.objects.all()
        ],
        "days": [
            {
                "id": day.key,
                "label": day.label,
                "date": day.date_label,
                "theme": day.theme,
                "agenda": [
                    {
                        "time": slot.time,
                        "end": slot.end,
                        "title": slot.title,
                        "note": slot.note,
                        "track": slot.track,
                    }
                    for slot in day.slots.all()
                ],
            }
            for day in models.AnniversaryDay.objects.prefetch_related("slots")
        ],
        "credit": event.credit,
    }
