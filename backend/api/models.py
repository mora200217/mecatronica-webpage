"""Modelos del CMS.

Todo el contenido editable del sitio vive aquí y se administra desde
/admin/. La malla curricular es la excepción: sigue en
`content/curriculum.json` porque se genera con un script.
"""

from django.db import models


class Singleton(models.Model):
    """Contenido del que solo existe una versión (una página, un ajuste)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # pragma: no cover - bloqueado en el admin
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Ordered(models.Model):
    """Se ordena a mano desde el admin arrastrando el número."""

    order = models.PositiveIntegerField("orden", default=0)

    class Meta:
        abstract = True
        ordering = ["order", "pk"]


class WithImage(models.Model):
    """Permite subir una foto o apuntar a una ruta ya existente."""

    image = models.ImageField("imagen", upload_to="subidas/", blank=True)
    image_url = models.CharField(
        "ruta de imagen",
        max_length=300,
        blank=True,
        help_text="Úsalo si la foto ya está en el sitio, por ejemplo /media/cyt.jpg",
    )

    class Meta:
        abstract = True

    @property
    def image_src(self) -> str:
        if self.image:
            return self.image.url
        return self.image_url


# --------------------------------------------------------------------------
# Ajustes generales
# --------------------------------------------------------------------------


class SiteSettings(Singleton):
    program = models.CharField("programa", max_length=120, default="Ingeniería Mecatrónica")
    faculty = models.CharField("facultad", max_length=120, default="Facultad de Ingeniería")
    university = models.CharField(
        "universidad", max_length=140, default="Universidad Nacional de Colombia"
    )
    campus = models.CharField("sede", max_length=80, default="Sede Bogotá")
    snies = models.CharField("SNIES", max_length=20, blank=True)
    sia = models.CharField("código SIA", max_length=20, blank=True)
    credits = models.PositiveIntegerField("créditos", default=179)
    semesters = models.PositiveIntegerField("semestres", default=10)
    created = models.PositiveIntegerField("año de creación", default=2001)
    title = models.CharField("título que otorga", max_length=140, blank=True)
    tagline = models.CharField("frase de la carrera", max_length=240, blank=True)

    birthday_years = models.PositiveIntegerField("cumpleaños: años", default=25)
    birthday_kicker = models.CharField("cumpleaños: antetítulo", max_length=120, blank=True)
    birthday_headline = models.CharField("cumpleaños: titular", max_length=240, blank=True)
    birthday_body = models.TextField("cumpleaños: texto", blank=True)

    contact_coordinator = models.CharField("coordinador", max_length=160, blank=True)
    contact_email = models.EmailField("correo", blank=True)
    contact_building = models.CharField("edificio", max_length=160, blank=True)
    contact_address = models.CharField("dirección", max_length=200, blank=True)
    contact_phone = models.CharField("teléfono", max_length=80, blank=True)

    disclaimer = models.TextField("aviso al pie", blank=True)

    class Meta:
        verbose_name = "ajustes del sitio"
        verbose_name_plural = "ajustes del sitio"

    def __str__(self):
        return "Ajustes del sitio"


class HeroSlide(Ordered, WithImage):
    kicker = models.CharField("antetítulo", max_length=120)
    title = models.CharField("titular", max_length=200)
    body = models.TextField("texto", blank=True)
    label = models.CharField(
        "etiqueta de la foto", max_length=140, blank=True, help_text="Se muestra arriba a la derecha"
    )
    accent = models.BooleanField(
        "destacado", default=False, help_text="Pinta el antetítulo con el color de la celebración"
    )
    cta_label = models.CharField("botón: texto", max_length=80, blank=True)
    cta_to = models.CharField(
        "botón: ruta interna", max_length=120, blank=True, help_text="Por ejemplo /programa"
    )
    cta_href = models.CharField(
        "botón: enlace o ancla", max_length=200, blank=True, help_text="Por ejemplo #aniversario"
    )

    class Meta(Ordered.Meta):
        verbose_name = "diapositiva del carrusel"
        verbose_name_plural = "carrusel de la portada"

    def __str__(self):
        return self.title


# --------------------------------------------------------------------------
# Noticias y eventos
# --------------------------------------------------------------------------


class NewsPost(WithImage):
    slug = models.SlugField("enlace", max_length=140, unique=True)
    title = models.CharField("título", max_length=240)
    kicker = models.CharField("sección", max_length=80, blank=True)
    date = models.DateField("fecha")
    excerpt = models.TextField("resumen", blank=True)
    body = models.TextField("cuerpo", blank=True, help_text="Separa los párrafos con una línea en blanco")
    published = models.BooleanField("publicada", default=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "noticia"
        verbose_name_plural = "noticias"

    def __str__(self):
        return self.title


class EventCategory(Ordered):
    slug = models.SlugField("identificador", max_length=40, unique=True)
    label = models.CharField("nombre", max_length=80)

    class Meta(Ordered.Meta):
        verbose_name = "tipo de evento"
        verbose_name_plural = "tipos de evento"

    def __str__(self):
        return self.label


class Event(Ordered):
    category = models.ForeignKey(
        EventCategory, verbose_name="tipo", on_delete=models.PROTECT, related_name="events"
    )
    month = models.CharField("mes", max_length=20)
    day = models.CharField("día", max_length=4)
    title = models.CharField("título", max_length=240)
    place = models.CharField("lugar", max_length=160, blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "evento"
        verbose_name_plural = "eventos"

    def __str__(self):
        return f"{self.day} {self.month} · {self.title}"


# --------------------------------------------------------------------------
# Egresados
# --------------------------------------------------------------------------


class AlumniPage(Singleton):
    note = models.TextField("nota de la página", blank=True)

    class Meta:
        verbose_name = "egresados: nota"
        verbose_name_plural = "egresados: nota"

    def __str__(self):
        return "Nota de egresados"


class Alumnus(Ordered):
    name = models.CharField("nombre", max_length=140)
    cohort = models.CharField("cohorte", max_length=20, blank=True)
    role = models.CharField("cargo", max_length=140, blank=True)
    company = models.CharField("empresa", max_length=180, blank=True)
    city = models.CharField("ciudad", max_length=80, blank=True)
    focus = models.CharField("temas", max_length=200, blank=True)
    linkedin = models.URLField("LinkedIn", max_length=300, blank=True)
    mentorship = models.BooleanField("abierto a mentoría", default=False)

    class Meta(Ordered.Meta):
        verbose_name = "egresado"
        verbose_name_plural = "egresados"

    def __str__(self):
        return self.name


# --------------------------------------------------------------------------
# Industria
# --------------------------------------------------------------------------


class IndustryPage(Singleton):
    pitch = models.TextField("presentación", blank=True)

    class Meta:
        verbose_name = "industria: presentación"
        verbose_name_plural = "industria: presentación"

    def __str__(self):
        return "Presentación de industria"


class IndustrySector(Ordered):
    name = models.CharField("sector", max_length=140)
    body = models.TextField("descripción", blank=True)
    examples = models.CharField(
        "ejemplos", max_length=240, blank=True, help_text="Sepáralos con comas"
    )

    class Meta(Ordered.Meta):
        verbose_name = "sector de industria"
        verbose_name_plural = "sectores de industria"

    def __str__(self):
        return self.name


class IndustryPartner(Ordered):
    name = models.CharField("aliado", max_length=180)
    role = models.CharField("qué hace con el programa", max_length=200, blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "aliado de industria"
        verbose_name_plural = "aliados de industria"

    def __str__(self):
        return self.name


# --------------------------------------------------------------------------
# Programa: docentes, laboratorios y grupos
# --------------------------------------------------------------------------


class ProgramPage(Singleton):
    about = models.TextField("sobre el programa", blank=True)

    class Meta:
        verbose_name = "programa: presentación"
        verbose_name_plural = "programa: presentación"

    def __str__(self):
        return "Presentación del programa"


class FacultyMember(Ordered):
    name = models.CharField("nombre", max_length=160)
    role = models.CharField("cargo", max_length=140, blank=True)
    area = models.CharField("área", max_length=200, blank=True)
    email = models.EmailField("correo", blank=True)
    real = models.BooleanField(
        "ficha verificada",
        default=False,
        help_text="Desmárcalo si es un perfil de ejemplo mientras consigues el dato real",
    )

    class Meta(Ordered.Meta):
        verbose_name = "docente"
        verbose_name_plural = "docentes"

    def __str__(self):
        return self.name


class Lab(Ordered):
    name = models.CharField("laboratorio", max_length=160)
    building = models.CharField("ubicación", max_length=120, blank=True)
    github = models.URLField("repositorio", blank=True)
    body = models.TextField("descripción", blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "laboratorio"
        verbose_name_plural = "laboratorios"

    def __str__(self):
        return self.name


class ResearchGroup(Ordered):
    name = models.CharField("grupo", max_length=180)
    line = models.CharField("línea de trabajo", max_length=220, blank=True)
    hermes = models.URLField("enlace Hermes", blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "grupo de investigación"
        verbose_name_plural = "grupos de investigación"

    def __str__(self):
        return self.name


# --------------------------------------------------------------------------
# Ofertas y tesis
# --------------------------------------------------------------------------


class Job(Ordered):
    title = models.CharField("cargo", max_length=200)
    company = models.CharField("empresa", max_length=200, blank=True)
    type = models.CharField("modalidad", max_length=80, blank=True)
    area = models.CharField("área", max_length=120, blank=True)
    deadline = models.DateField("cierra el", null=True, blank=True)
    body = models.TextField("descripción", blank=True)
    published = models.BooleanField("publicada", default=True)

    class Meta(Ordered.Meta):
        verbose_name = "oferta"
        verbose_name_plural = "ofertas"

    def __str__(self):
        return self.title


class Thesis(Ordered):
    year = models.PositiveIntegerField("año")
    title = models.CharField("título", max_length=260)
    authors = models.CharField("autores", max_length=200, blank=True)
    modality = models.CharField("modalidad", max_length=120, blank=True)
    tags = models.CharField("etiquetas", max_length=200, blank=True, help_text="Sepáralas con comas")

    class Meta:
        ordering = ["-year", "order", "pk"]
        verbose_name = "tesis"
        verbose_name_plural = "tesis"

    def __str__(self):
        return self.title


# --------------------------------------------------------------------------
# Puentes (redirecciones a sistemas UNAL)
# --------------------------------------------------------------------------


class Redirect(Ordered):
    slug = models.SlugField("atajo", max_length=60, unique=True, help_text="Queda en /go/<atajo>/")
    title = models.CharField("nombre", max_length=160)
    group = models.CharField("grupo", max_length=80, blank=True)
    description = models.CharField("descripción", max_length=240, blank=True)
    url = models.URLField("destino", max_length=500)

    class Meta(Ordered.Meta):
        verbose_name = "puente"
        verbose_name_plural = "puentes"

    def __str__(self):
        return self.title


# --------------------------------------------------------------------------
# Historia
# --------------------------------------------------------------------------


class HistoryPage(Singleton):
    intro = models.TextField("introducción", blank=True)

    class Meta:
        verbose_name = "historia: introducción"
        verbose_name_plural = "historia: introducción"

    def __str__(self):
        return "Introducción de historia"


class HistoryStat(Ordered):
    KIND_CHOICES = [("count", "Cuenta desde cero"), ("year", "Es un año")]

    key = models.SlugField("identificador", max_length=40, unique=True)
    value = models.IntegerField("número")
    kind = models.CharField("tipo", max_length=10, choices=KIND_CHOICES, default="count")
    label = models.CharField("qué significa", max_length=120)
    detail = models.CharField("detalle", max_length=240, blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "dato clave"
        verbose_name_plural = "historia: datos clave"

    def __str__(self):
        return f"{self.value} {self.label}"


class HistoryEra(Ordered):
    slug = models.SlugField("identificador", max_length=40, unique=True)
    label = models.CharField("nombre", max_length=80)
    range_label = models.CharField("rango de años", max_length=40, blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "época"
        verbose_name_plural = "historia: épocas"

    def __str__(self):
        return self.label


class HistoryMilestone(Ordered, WithImage):
    era = models.ForeignKey(
        HistoryEra, verbose_name="época", on_delete=models.PROTECT, related_name="milestones"
    )
    year = models.CharField("año", max_length=20, help_text="Puede ser un rango, como 2009–2014")
    title = models.CharField("título", max_length=200)
    body = models.TextField("texto", blank=True)
    figure_value = models.CharField("dato destacado", max_length=40, blank=True)
    figure_label = models.CharField("qué es el dato", max_length=120, blank=True)
    tags = models.CharField("etiquetas", max_length=200, blank=True, help_text="Sepáralas con comas")

    class Meta(Ordered.Meta):
        verbose_name = "hito"
        verbose_name_plural = "historia: línea de tiempo"

    def __str__(self):
        return f"{self.year} · {self.title}"


class GalleryPhoto(Ordered, WithImage):
    title = models.CharField("título", max_length=160)
    caption = models.CharField("pie de foto", max_length=300, blank=True)
    credit = models.CharField("crédito", max_length=160, blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "foto"
        verbose_name_plural = "historia: galería"

    def __str__(self):
        return self.title


# --------------------------------------------------------------------------
# Aniversario
# --------------------------------------------------------------------------


class AnniversaryEvent(Singleton, WithImage):
    kicker = models.CharField("antetítulo", max_length=80, blank=True)
    headline = models.CharField("titular", max_length=200, blank=True)
    lead = models.TextField("entradilla", blank=True)
    years = models.PositiveIntegerField("años que cumple", default=25)

    logo = models.ImageField("logo (fondo oscuro)", upload_to="aniversario/", blank=True)
    logo_url = models.CharField("ruta del logo", max_length=300, blank=True)
    logo_ink = models.ImageField("logo (fondo claro)", upload_to="aniversario/", blank=True)
    logo_ink_url = models.CharField("ruta del logo claro", max_length=300, blank=True)

    starts_at = models.DateTimeField("empieza", null=True, blank=True)
    ends_at = models.DateTimeField("termina", null=True, blank=True)
    date_label = models.CharField("fechas en texto", max_length=120, blank=True)
    venue = models.CharField("lugar", max_length=200, blank=True)

    cta_label = models.CharField("botón: texto", max_length=80, blank=True)
    cta_to = models.CharField("botón: ruta interna", max_length=120, blank=True)

    contact_email = models.EmailField("correo", blank=True)
    contact_phone = models.CharField("teléfono", max_length=80, blank=True)
    credit = models.CharField("línea de crédito", max_length=240, blank=True)

    class Meta:
        verbose_name = "aniversario"
        verbose_name_plural = "aniversario"

    def __str__(self):
        return self.headline or "Aniversario"

    @property
    def logo_src(self) -> str:
        return self.logo.url if self.logo else self.logo_url

    @property
    def logo_ink_src(self) -> str:
        return self.logo_ink.url if self.logo_ink else self.logo_ink_url


class AnniversaryHighlight(Ordered):
    key = models.SlugField("identificador", max_length=40, unique=True)
    title = models.CharField("título", max_length=140)
    body = models.TextField("texto", blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "destacado del aniversario"
        verbose_name_plural = "aniversario: destacados"

    def __str__(self):
        return self.title


class AnniversaryDay(Ordered):
    key = models.SlugField("identificador", max_length=40, unique=True)
    label = models.CharField("pestaña", max_length=60)
    date_label = models.CharField("fecha", max_length=120, blank=True)
    theme = models.CharField("tema del día", max_length=160, blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "día del aniversario"
        verbose_name_plural = "aniversario: días"

    def __str__(self):
        return self.label


class AgendaSlot(Ordered):
    TRACK_CHOICES = [
        ("acto", "Acto institucional"),
        ("industria", "Industria"),
        ("egresados", "Egresados"),
        ("estudiantes", "Estudiantes"),
        ("foro", "Foro"),
        ("pausa", "Pausa"),
    ]

    day = models.ForeignKey(
        AnniversaryDay, verbose_name="día", on_delete=models.CASCADE, related_name="slots"
    )
    time = models.CharField("empieza", max_length=10)
    end = models.CharField("termina", max_length=10, blank=True)
    title = models.CharField("actividad", max_length=240)
    note = models.CharField("detalle", max_length=200, blank=True)
    track = models.CharField("franja", max_length=20, choices=TRACK_CHOICES, default="acto")

    class Meta(Ordered.Meta):
        verbose_name = "bloque de agenda"
        verbose_name_plural = "bloques de agenda"

    def __str__(self):
        return f"{self.time} · {self.title}"
