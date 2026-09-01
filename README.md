# Ingeniería Mecatrónica UNAL — sitio MVP

Sitio de la carrera (Pumpleaños 25) pensado para quedarse: estudiantes, egresados y la siguiente generación que lo va a editar.

## Qué hay

| Capa | Rol |
| --- | --- |
| `frontend/` | React + Vite. Pestañas, malla, noticias. |
| `backend/` | Django. API JSON + orquestador `/go/<slug>/`. |
| `backend/content/*.json` | CMS de pobre: editas el archivo y se refleja en la web. |
| Fotos | Wikimedia Commons, campus y Facultad de Ingeniería, en `frontend/public/media/`. |

## Cómo correrlo

```bash
# API
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 8000

# Web (otra terminal)
cd frontend
npm install
npm run dev
```

Abre [http://localhost:5173](http://localhost:5173). Vite reenvía `/api` y `/go` a Django.

## Cómo editar sin tocar React

- Noticias / blog: `backend/content/news.json`
- Eventos: `events.json`
- Egresados, ofertas, tesis, industria, historia, programa: archivos homónimos
- Puentes (redirecciones UNAL): `redirects.json`
- Malla del explorador: regenera con `python backend/content/_build_curriculum.py` o edita `curriculum.json`

La malla del explorador es **ilustrativa** (179 créditos, 10 semestres). El PDF oficial está en Puentes → *Malla curricular*.

## Orquestador

`GET /go/sia/` redirige a SIA. Lo mismo para correo, Hermes, PEP, malla PDF, etc. La UI está en `/puentes`.

## Qué sigue (Supabase)

Cada JSON es una tabla futura (`posts`, `alumni`, `jobs`, `courses`, `redirects`). Django puede seguir siendo el orquestador y leer de Supabase en vez del disco. No hay que rehacer las pantallas.

## Créditos de fotos

Imágenes de [Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:Edificio_de_Ingenier%C3%ADa_-_Universidad_Nacional_de_Colombia,_Bogot%C3%A1) (Facultad de Ingeniería, Edificio CyT, aulas).
