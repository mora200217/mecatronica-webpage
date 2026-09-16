from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from . import models

admin.site.site_header = "Ingeniería Mecatrónica UNAL"
admin.site.site_title = "Mecatrónica · CMS"
admin.site.index_title = "Edita el contenido del sitio. La malla curricular se queda fuera: se genera con un script."
admin.site.site_url = settings.SITE_URL


class SingletonAdmin(admin.ModelAdmin):
    """Una sola ficha: no se puede crear ni borrar, solo editar."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        self.model.load()
        return super().changelist_view(request, extra_context)


class ImagePreviewMixin:
    save_on_top = True
    @admin.display(description="vista previa")
    def preview(self, obj):
        src = obj.image_src
        if not src:
            return "—"
        return format_html('<img src="{}" style="height:56px;border:1px solid #ddd" />', src)


# --------------------------------------------------------------------------
# Portada y ajustes
# --------------------------------------------------------------------------


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Identidad", {"fields": ("program", "faculty", "university", "campus", "tagline")}),
        ("Datos del programa", {"fields": ("snies", "sia", "credits", "semesters", "created", "title")}),
        (
            "Cumpleaños",
            {"fields": ("birthday_years", "birthday_kicker", "birthday_headline", "birthday_body")},
        ),
        (
            "Contacto",
            {
                "fields": (
                    "contact_coordinator",
                    "contact_email",
                    "contact_building",
                    "contact_address",
                    "contact_phone",
                )
            },
        ),
        ("Pie", {"fields": ("disclaimer",)}),
    )


@admin.register(models.HeroSlide)
class HeroSlideAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title", "kicker", "accent", "order", "preview")
    list_editable = ("order",)
    fieldsets = (
        ("Texto", {"fields": ("kicker", "title", "body", "label", "accent")}),
        ("Imagen", {"fields": ("image", "image_url")}),
        ("Botón", {"fields": ("cta_label", "cta_to", "cta_href")}),
        ("Posición", {"fields": ("order",)}),
    )


# --------------------------------------------------------------------------
# Noticias y eventos
# --------------------------------------------------------------------------


@admin.register(models.NewsPost)
class NewsPostAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title", "kicker", "date", "published", "preview")
    list_filter = ("published", "kicker")
    search_fields = ("title", "excerpt", "body")
    date_hierarchy = "date"
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Noticia", {"fields": ("title", "slug", "kicker", "date", "published")}),
        ("Contenido", {"fields": ("excerpt", "body")}),
        ("Imagen", {"fields": ("image", "image_url")}),
    )


@admin.register(models.EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("label", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("label",)}


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "month", "day", "category", "place", "order")
    list_editable = ("order",)
    list_filter = ("category", "month")
    search_fields = ("title", "place")


# --------------------------------------------------------------------------
# Egresados
# --------------------------------------------------------------------------


@admin.register(models.AlumniPage)
class AlumniPageAdmin(SingletonAdmin):
    pass


@admin.register(models.Alumnus)
class AlumnusAdmin(admin.ModelAdmin):
    list_display = ("name", "cohort", "role", "company", "city", "mentorship", "order")
    list_editable = ("order",)
    list_filter = ("mentorship", "city", "cohort")
    search_fields = ("name", "company", "focus")


# --------------------------------------------------------------------------
# Industria
# --------------------------------------------------------------------------


@admin.register(models.IndustryPage)
class IndustryPageAdmin(SingletonAdmin):
    pass


@admin.register(models.IndustrySector)
class IndustrySectorAdmin(admin.ModelAdmin):
    list_display = ("name", "examples", "order")
    list_editable = ("order",)


@admin.register(models.IndustryPartner)
class IndustryPartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    list_editable = ("order",)


# --------------------------------------------------------------------------
# Programa
# --------------------------------------------------------------------------


@admin.register(models.ProgramPage)
class ProgramPageAdmin(SingletonAdmin):
    pass


@admin.register(models.FacultyMember)
class FacultyMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "area", "email", "real", "order")
    list_editable = ("order",)
    list_filter = ("real",)
    search_fields = ("name", "area")


@admin.register(models.Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ("name", "building", "order")
    list_editable = ("order",)


@admin.register(models.ResearchGroup)
class ResearchGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "line", "order")
    list_editable = ("order",)


# --------------------------------------------------------------------------
# Ofertas, tesis y puentes
# --------------------------------------------------------------------------


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "type", "area", "deadline", "published", "order")
    list_editable = ("order",)
    list_filter = ("published", "type", "area")
    search_fields = ("title", "company", "body")


@admin.register(models.Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "authors", "modality")
    list_filter = ("year", "modality")
    search_fields = ("title", "authors", "tags")


@admin.register(models.Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "group", "url", "order")
    list_editable = ("order",)
    list_filter = ("group",)
    prepopulated_fields = {"slug": ("title",)}


# --------------------------------------------------------------------------
# Historia
# --------------------------------------------------------------------------


@admin.register(models.HistoryPage)
class HistoryPageAdmin(SingletonAdmin):
    pass


@admin.register(models.HistoryStat)
class HistoryStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "kind", "order")
    list_editable = ("order",)


@admin.register(models.HistoryEra)
class HistoryEraAdmin(admin.ModelAdmin):
    list_display = ("label", "range_label", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("label",)}


@admin.register(models.HistoryMilestone)
class HistoryMilestoneAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("year", "title", "era", "order", "preview")
    list_editable = ("order",)
    list_filter = ("era",)
    fieldsets = (
        ("Hito", {"fields": ("year", "era", "title", "body", "tags")}),
        ("Dato destacado", {"fields": ("figure_value", "figure_label")}),
        ("Imagen", {"fields": ("image", "image_url")}),
        ("Posición", {"fields": ("order",)}),
    )


@admin.register(models.GalleryPhoto)
class GalleryPhotoAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title", "credit", "order", "preview")
    list_editable = ("order",)
    fields = ("title", "caption", "credit", "image", "image_url", "order")


# --------------------------------------------------------------------------
# Aniversario
# --------------------------------------------------------------------------


@admin.register(models.AnniversaryEvent)
class AnniversaryEventAdmin(SingletonAdmin):
    fieldsets = (
        ("Encabezado", {"fields": ("kicker", "headline", "lead", "years")}),
        ("Cuándo y dónde", {"fields": ("starts_at", "ends_at", "date_label", "venue")}),
        ("Imágenes", {"fields": ("logo", "logo_url", "logo_ink", "logo_ink_url", "image", "image_url")}),
        ("Botón", {"fields": ("cta_label", "cta_to")}),
        ("Contacto y crédito", {"fields": ("contact_email", "contact_phone", "credit")}),
    )


@admin.register(models.AnniversaryHighlight)
class AnniversaryHighlightAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    prepopulated_fields = {"key": ("title",)}


class AgendaSlotInline(admin.TabularInline):
    model = models.AgendaSlot
    extra = 1
    fields = ("order", "time", "end", "title", "note", "track")
    ordering = ("order",)


@admin.register(models.AnniversaryDay)
class AnniversaryDayAdmin(admin.ModelAdmin):
    list_display = ("label", "date_label", "theme", "order")
    list_editable = ("order",)
    prepopulated_fields = {"key": ("label",)}
    inlines = [AgendaSlotInline]


# El índice del admin agrupa por sección del sitio, no por app técnica.
ADMIN_GROUPS = [
    ("Portada", ["SiteSettings", "HeroSlide"]),
    ("Aniversario", ["AnniversaryEvent", "AnniversaryHighlight", "AnniversaryDay"]),
    ("Noticias y eventos", ["NewsPost", "EventCategory", "Event"]),
    ("Egresados", ["AlumniPage", "Alumnus"]),
    ("Industria y empresas", ["IndustryPage", "IndustrySector", "IndustryPartner"]),
    ("Programa", ["ProgramPage", "FacultyMember", "Lab", "ResearchGroup"]),
    ("Ofertas y tesis", ["Job", "Thesis"]),
    ("Historia", ["HistoryPage", "HistoryStat", "HistoryEra", "HistoryMilestone", "GalleryPhoto"]),
    ("Puentes UNAL", ["Redirect"]),
    ("Acceso", ["User", "Group"]),
]


def _grouped_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    if app_label:
        return sorted(app_dict.values(), key=lambda item: item["name"].lower())

    by_name = {}
    for app in app_dict.values():
        for model in app["models"]:
            by_name[model["object_name"]] = model

    grouped = []
    used = set()
    for label, names in ADMIN_GROUPS:
        models_out = [by_name[name] for name in names if name in by_name]
        if not models_out:
            continue
        used.update(names)
        grouped.append(
            {
                "name": label,
                "app_label": label.lower().replace(" ", "_"),
                "app_url": "/admin/",
                "has_module_perms": True,
                "models": models_out,
            }
        )
    leftover = [item for name, item in by_name.items() if name not in used]
    if leftover:
        grouped.append(
            {
                "name": "Otros",
                "app_label": "otros",
                "app_url": "/admin/",
                "has_module_perms": True,
                "models": leftover,
            }
        )
    return grouped


admin.AdminSite.get_app_list = _grouped_app_list
