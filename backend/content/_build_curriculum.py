import json
from pathlib import Path

courses = []


def add(cid, name, credits, semester, component, area, prereqs, summary, note=""):
    item = {
        "id": cid,
        "name": name,
        "credits": credits,
        "semester": semester,
        "component": component,
        "area": area,
        "prereqs": prereqs,
        "summary": summary,
    }
    if note:
        item["note"] = note
    courses.append(item)


F, D, L = "fundamentacion", "disciplinar", "libre"
PROG70 = "Requiere haber aprobado el 70% del programa (unos 125 créditos)."

# Semestre I — 15
add("1000004", "Cálculo diferencial", 4, 1, F, "matematicas", [], "Límites, derivadas y modelado de cambio.")
add("2015734", "Programación de computadores", 3, 1, F, "informatica", [], "Algoritmos y pensamiento computacional.")
add("2016509", "Taller de ingeniería electrónica", 2, 1, D, "electronica", [], "Práctica inicial de circuitos y laboratorio.")
add("2015702", "Ingeniería y desarrollo sostenible", 3, 1, D, "investigacion", [], "Impacto de la tecnología y el oficio del ingeniero.")
add("2015711", "Dibujo básico", 3, 1, F, "expresion", [], "Representación gráfica para ingeniería.")

# Semestre II — 15
add("1000005", "Cálculo integral", 4, 2, F, "matematicas", ["1000004"], "Integrales, series y aplicaciones.")
add("1000003", "Álgebra lineal", 4, 2, F, "matematicas", [], "Vectores, matrices y sistemas lineales.")
add("1000019", "Fundamentos de mecánica", 4, 2, F, "fisica", ["1000004"], "Cinemática, dinámica y energía.")
add("2017278", "Tecnología mecánica básica", 3, 2, D, "materiales", [], "Procesos y herramientas de taller mecánico.")

# Semestre III — 20
add("1000006", "Cálculo en varias variables", 4, 3, F, "matematicas", ["1000005"], "Campos, integrales múltiples y cálculo vectorial.")
add("1000013", "Probabilidad y estadística fundamental", 3, 3, F, "matematicas", ["1000003"], "Incertidumbre, muestreo y decisión.")
add("1000017", "Fundamentos de electricidad y magnetismo", 4, 3, F, "fisica", ["1000019"], "Campos, circuitos y fuerza electromagnética.")
add("2016489", "Circuitos eléctricos I", 3, 3, D, "electronica", ["2016509"], "Leyes de Kirchhoff, DC y transitorios.")
add("2016640", "Principios de estática", 3, 3, D, "diseno", ["1000019", "1000003"], "Equilibrio de partículas y cuerpos rígidos.")
add("1000024", "Principios de química", 3, 3, F, "quimica", [], "Estructura de la materia para materiales y procesos.")

# Semestre IV — 20
add("1000007", "Ecuaciones diferenciales", 4, 4, F, "matematicas", ["1000006"], "EDO, Laplace y modelos de sistemas.")
add("LIB-IV-A", "Libre elección", 3, 4, L, "libre", [], "Asignatura de libre elección del componente flexible.")
add("2016375", "Programación orientada a objetos", 3, 4, D, "informatica", ["2015734"], "Diseño de software para sistemas físicos.")
add("2016495", "Electrónica análoga I", 4, 4, D, "electronica", ["2016489"], "Diodos, transistores y acondicionamiento.")
add("2017271", "Principios de dinámica", 3, 4, D, "diseno", ["2016640"], "Cinemática y cinética de máquinas.")
add("LIB-IV-B", "Libre elección", 3, 4, L, "libre", [], "Asignatura de libre elección del componente flexible.")

# Semestre V — 19
add("2015703", "Variable compleja", 4, 5, F, "matematicas", ["1000007"], "Números complejos, funciones y transformadas.")
add("OPT-FIS", "Optativa de física", 3, 5, F, "fisica", ["1000017"], "Optativa de fundamentación en física (3 o 4 créditos según la oferta).")
add("2016506", "Señales y sistemas I", 3, 5, D, "control", ["1000007"], "Sistemas LTI, tiempo continuo y transformadas.")
add("2016699", "Estructura de datos", 3, 5, D, "informatica", ["2016375"], "Colecciones, complejidad y bases para software de ingeniería.")
add("2017277", "Resistencia de materiales", 3, 5, D, "diseno", ["2016640"], "Esfuerzo, deformación y falla.")
add("2017256", "Ciencia e ingeniería de materiales", 3, 5, D, "materiales", ["1000024", "2017278"], "Metales, polímeros y selección de materiales.")

# Semestre VI — 19
add("2015159", "Ingeniería económica", 3, 6, F, "gestion", ["2015703"], "Evaluación de proyectos y decisión económica.")
add("2016507", "Señales y sistemas II", 3, 6, D, "control", ["2016506"], "Tiempo discreto, muestreo y respuesta en frecuencia.")
add("2016498", "Electrónica digital I", 4, 6, D, "electronica", ["2016495"], "Lógica, HDL y sistemas digitales.")
add("2024045", "Taller de proyectos interdisciplinarios", 3, 6, D, "investigacion", ["2016699"], "Problema real con otras ingenierías. Requiere 52 créditos del programa.")
add("2017282", "Diseño mecatrónico", 3, 6, D, "diseno", ["2017271", "2017277"], "Metodología de producto que integra mecanismo, electrónica y control.")
add("2017273", "Optativa de materiales y manufactura", 3, 6, D, "materiales", ["2017256"], "Optativa disciplinar de la agrupación de materiales y procesos.")

# Semestre VII — 19
add("OPT-ECO", "Optativa de ciencias económicas", 3, 7, F, "gestion", ["2015159"], "Optativa de fundamentación en ciencias administrativas y económicas.")
add("2016493", "Control", 4, 7, D, "control", ["2016507"], "Lazo cerrado, PID y estabilidad.")
add("2017287", "Sensores y actuadores", 3, 7, D, "control", ["2016498"], "Transducción, motores y acondicionamiento.")
add("2025967", "Redes de computadores", 3, 7, D, "informatica", ["2024045"], "Comunicación de datos para sistemas distribuidos.")
add("2016753", "Microcontroladores I", 3, 7, D, "electronica", ["2016498"], "Firmware, timers, ADC y buses.")
add("OPT-INFO", "Optativa de informática", 3, 7, F, "informatica", ["2015734"], "Optativa de fundamentación en informática y herramientas de ingeniería.")

# Semestre VIII — 18
add("LIB-VIII-A", "Libre / profundización", 3, 8, L, "libre", [], "Libre elección o profundización.", PROG70)
add("2017770", "Robótica", 3, 8, D, "control", ["2016493"], "Cinemática, trayectoria y celdas robotizadas.")
add("OPT-AUTO", "Optativa de automatización y control", 3, 8, D, "control", ["2016493"], "Optativa disciplinar de automatización, control y robótica.")
add("LIB-VIII-B", "Libre / profundización", 3, 8, L, "libre", [], "Libre elección o profundización.", PROG70)
add("2017288", "Servomecanismos", 3, 8, D, "diseno", ["2016753", "2017282"], "Accionamientos, lazo de posición y máquinas de movimiento.")
add("LIB-VIII-C", "Libre / profundización", 3, 8, L, "libre", [], "Libre elección o profundización.", PROG70)

# Semestre IX — 16
add("LIB-IX-A", "Libre / profundización", 3, 9, L, "libre", [], "Libre elección o profundización (3 o 6 créditos según la oferta).", PROG70)
add("LIB-IX-B", "Libre / profundización", 3, 9, L, "libre", [], "Libre elección o profundización.", PROG70)
add("LIB-IX-C", "Libre / profundización", 3, 9, L, "libre", [], "Libre elección o profundización.", PROG70)
add("2017275", "Proyecto aplicado de ingeniería", 4, 9, D, "investigacion", ["2017282", "2024045"], "Diseñar y construir una máquina en equipo. Requiere 65 créditos del programa.")
add("2017280", "Automatización de procesos de manufactura", 3, 9, D, "materiales", ["2017278"], "Celdas, CNC y flujo de planta.")

# Semestre X — 18
add("LIB-X-A", "Libre / profundización", 3, 10, L, "libre", [], "Libre elección o profundización.", PROG70)
add("LIB-X-B", "Libre elección", 9, 10, L, "libre", [], "Bloque flexible para completar el 20% de libre elección.")
add("2017297", "Trabajo de grado", 6, 10, D, "investigacion", ["2017275"], "Formulación, prototipo y sustentación. Requiere 69 créditos del programa.")

payload = {
    "disclaimer": "Plan de estudios del Acuerdo 6 de 2022 del Consejo de Facultad de Ingeniería. 179 créditos: 56 de fundamentación (47 obligatorios y 9 optativos), 87 disciplinares (81 obligatorios y 6 optativos) y 36 de libre elección. Los prerrequisitos siguen las flechas del PDF oficial; la lengua extranjera (12 créditos extra, 191 en total) no entra en este tablero.",
    "officialPdf": "/go/malla-oficial/",
    "components": [
        {"id": "fundamentacion", "label": "Fundamentación", "credits": 56, "pct": "31%"},
        {"id": "disciplinar", "label": "Disciplinar", "credits": 87, "pct": "49%"},
        {"id": "libre", "label": "Libre elección", "credits": 36, "pct": "20%"},
    ],
    "areas": [
        {"id": "matematicas", "label": "Matemáticas, probabilidad y estadística"},
        {"id": "fisica", "label": "Física"},
        {"id": "quimica", "label": "Química"},
        {"id": "expresion", "label": "Expresión gráfica"},
        {"id": "informatica", "label": "Informática"},
        {"id": "electronica", "label": "Ingeniería electrónica"},
        {"id": "diseno", "label": "Ingeniería de diseño"},
        {"id": "control", "label": "Automatización, control y robótica"},
        {"id": "materiales", "label": "Materiales y manufactura"},
        {"id": "investigacion", "label": "Investigación e innovación"},
        {"id": "gestion", "label": "Ciencias administrativas y económicas"},
        {"id": "libre", "label": "Libre elección"},
    ],
    "courses": courses,
    "totals": {
        "credits": sum(c["credits"] for c in courses),
        "count": len(courses),
    },
}

path = Path(__file__).parent / "curriculum.json"
path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(payload["totals"])
print("por semestre:", {s: sum(c["credits"] for c in courses if c["semester"] == s) for s in range(1, 11)})
print("componentes:", {k: sum(c["credits"] for c in courses if c["component"] == k) for k in (F, D, L)})
