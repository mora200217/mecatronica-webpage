import json
from pathlib import Path

courses = []


def add(cid, name, credits, semester, component, area, prereqs, summary):
    courses.append(
        {
            "id": cid,
            "name": name,
            "credits": credits,
            "semester": semester,
            "component": component,
            "area": area,
            "prereqs": prereqs,
            "summary": summary,
        }
    )


F, D, L = "fundamentacion", "disciplinar", "libre"

add("INTRO", "Ingeniería y desarrollo sostenible", 3, 1, D, "integracion", [], "Panorama de la mecatrónica y el impacto de la tecnología.")
add("CALC1", "Cálculo diferencial", 4, 1, F, "matematicas", [], "Límites, derivadas y modelado de cambio.")
add("ALGLIN", "Álgebra lineal", 4, 1, F, "matematicas", [], "Vectores, matrices y sistemas lineales.")
add("QUIM", "Química básica", 3, 1, F, "ciencias", [], "Estructura de la materia para materiales y procesos.")
add("COMU", "Competencias comunicativas", 3, 1, F, "contexto", [], "Escritura y oralidad para ingeniería.")

add("CALC2", "Cálculo integral", 4, 2, F, "matematicas", ["CALC1"], "Integrales, series y aplicaciones.")
add("FISMEC", "Física mecánica", 4, 2, F, "ciencias", ["CALC1"], "Cinemática, dinámica y energía.")
add("PROG", "Programación de computadores", 3, 2, F, "computacion", [], "Algoritmos, Python/C y pensamiento computacional.")
add("DIB", "Dibujo de ingeniería", 3, 2, F, "diseno", [], "Representación gráfica y CAD 2D/3D.")
add("ECO", "Economía y gestión", 3, 2, F, "gestion", [], "Costos, decisión y entorno productivo.")
add("OPT1", "Optativa de fundamentación I", 3, 2, F, "matematicas", ["CALC1"], "Estadística, biología o herramienta de ingeniería.")

add("CALC3", "Cálculo en varias variables", 4, 3, F, "matematicas", ["CALC2"], "Campos, integrales múltiples y vectorial.")
add("FISEM", "Física de electricidad y magnetismo", 4, 3, F, "ciencias", ["FISMEC"], "Campos, circuitos y fuerza electromagnética.")
add("ESTAT", "Estática", 3, 3, D, "diseno", ["FISMEC", "ALGLIN"], "Equilibrio de partículas y cuerpos rígidos.")
add("CIR1", "Circuitos eléctricos I", 3, 3, D, "electronica", ["FISEM"], "Leyes de Kirchhoff, DC y transitorios.")
add("MATER", "Materiales de ingeniería", 3, 3, D, "manufactura", ["QUIM"], "Metales, polímeros y selección de materiales.")

add("EDO", "Ecuaciones diferenciales", 4, 4, F, "matematicas", ["CALC3"], "EDO, Laplace y modelos de sistemas.")
add("DIN", "Dinámica", 3, 4, D, "diseno", ["ESTAT"], "Cinemática y cinética de máquinas.")
add("TERMO", "Termodinámica", 3, 4, D, "manufactura", ["FISMEC"], "Energía, ciclos y conversión.")
add("CIR2", "Circuitos eléctricos II", 3, 4, D, "electronica", ["CIR1"], "AC, potencia y acoplamiento.")
add("OOP", "Programación orientada a objetos", 3, 4, D, "computacion", ["PROG"], "Diseño de software para sistemas físicos.")
add("PROB", "Probabilidad y estadística", 3, 4, F, "matematicas", ["CALC2"], "Incertidumbre, diseño de experimentos y calidad.")

add("SENALES", "Señales y sistemas", 3, 5, D, "control", ["EDO"], "LTI, Fourier y respuesta en frecuencia.")
add("SOLIDOS", "Mecánica de sólidos", 3, 5, D, "diseno", ["ESTAT"], "Esfuerzo, deformación y falla.")
add("EANA", "Electrónica analógica", 3, 5, D, "electronica", ["CIR2"], "Diodos, transistores y acondicionamiento.")
add("MANUF", "Procesos de manufactura", 3, 5, D, "manufactura", ["MATER"], "Arranque, conformado y calidad.")
add("MECAN", "Mecanismos", 3, 5, D, "diseno", ["DIN"], "Cadenas cinemáticas y síntesis.")

add("CTRL", "Control", 3, 6, D, "control", ["SENALES"], "Lazo cerrado, PID y estabilidad.")
add("EDIG", "Electrónica digital", 3, 6, D, "electronica", ["EANA"], "Lógica, HDL y sistemas digitales.")
add("ELEM", "Diseño de elementos de máquinas", 3, 6, D, "diseno", ["SOLIDOS", "MECAN"], "Ejes, engranajes, uniones y fatiga.")
add("SENS", "Sensores y actuadores", 3, 6, D, "control", ["EANA"], "Transducción, motores y válvulas.")
add("NUM", "Métodos numéricos", 3, 6, F, "matematicas", ["PROG", "EDO"], "Discretización y simulación.")

add("MCU", "Microcontroladores", 3, 7, D, "computacion", ["EDIG", "OOP"], "Firmware, timers, ADC y buses.")
add("ROB", "Robótica", 3, 7, D, "control", ["CTRL", "MECAN"], "Cinemática, trayectoria y celdas.")
add("AUTO", "Automatización industrial", 3, 7, D, "control", ["SENS", "CTRL"], "PLC, HMI y redes de planta.")
add("DM1", "Diseño mecatrónico I", 3, 7, D, "integracion", ["ELEM", "SENS"], "Metodología de producto integrado.")
add("INGECO", "Ingeniería económica", 3, 7, F, "gestion", ["ECO"], "Evaluación de proyectos tecnológicos.")
add("OPT2", "Optativa disciplinar", 3, 7, D, "control", ["CTRL"], "Control moderno, visión o redes industriales.")

add("EMB", "Sistemas embebidos", 3, 8, D, "computacion", ["MCU"], "RTOS, hardware-software y HMI.")
add("MOTION", "Control de movimiento", 3, 8, D, "control", ["CTRL", "ROB"], "Servos, interpolación y safety.")
add("CIMS", "Manufactura automatizada", 3, 8, D, "manufactura", ["AUTO", "MANUF"], "Celdas, CNC y flujo de planta.")
add("PAI", "Proyecto aplicado de ingeniería", 4, 8, D, "integracion", ["DM1"], "Diseñar y construir una máquina en equipo.")
add("TALLER", "Taller de proyectos interdisciplinarios", 3, 8, D, "integracion", ["INTRO"], "Problema real con otras ingenierías.")
add("LIB0", "Libre elección — profundización temprana", 3, 8, L, "libre", [], "Semillero, práctica o cátedra de facultad.")

add("ELE1", "Electiva de profundización I", 3, 9, L, "libre", [], "Robótica avanzada, visión, IoT o biomecánica.")
add("ELE2", "Electiva de profundización II", 3, 9, L, "libre", [], "Línea de maestría o asignatura de otro currículo.")
add("CTX1", "Cátedra de contexto / sede", 3, 9, L, "libre", [], "Ciudad, territorio y ética pública.")
add("TG1", "Trabajo de grado I", 4, 9, D, "integracion", ["PAI"], "Formulación, estado del arte y prototipo inicial.")
add("LIB1", "Libre elección I", 3, 9, L, "libre", [], "Emprendimiento, arte, lengua o semillero.")

add("ELE3", "Electiva de profundización III", 3, 10, L, "libre", ["ELE1"], "Cierre de línea de profundización.")
add("LIB2", "Libre elección II", 3, 10, L, "libre", [], "Movilidad, cátedra o práctica.")
add("LIB3", "Libre elección III", 3, 10, L, "libre", [], "Complemento flexible del 20%.")
add("TG2", "Trabajo de grado II", 6, 10, D, "integracion", ["TG1"], "Implementación, evaluación y sustentación.")
add("ETICA", "Ética, ambiente y ejercicio profesional", 3, 10, L, "contexto", ["INGECO"], "Impacto, norma y oficio del ingeniero.")
add("LIB4", "Libre elección IV", 5, 10, L, "libre", [], "Bloque flexible para completar el 20% de libre elección.")

payload = {
    "disclaimer": "Explorador ilustrativo para el MVP. La malla oficial vigente es el Acuerdo 6 de 2022 (PDF en Puentes). Nombres y prerrequisitos se acercan a la estructura pública del programa (179 créditos, 10 semestres) para que la herramienta se sienta usable.",
    "officialPdf": "/go/malla-oficial/",
    "components": [
        {"id": "fundamentacion", "label": "Fundamentación", "credits": 56, "pct": "31%"},
        {"id": "disciplinar", "label": "Disciplinar / profesional", "credits": 87, "pct": "48%"},
        {"id": "libre", "label": "Libre elección", "credits": 36, "pct": "20%"},
    ],
    "areas": [
        {"id": "matematicas", "label": "Matemáticas"},
        {"id": "ciencias", "label": "Ciencias"},
        {"id": "computacion", "label": "Computación"},
        {"id": "electronica", "label": "Electrónica"},
        {"id": "diseno", "label": "Diseño"},
        {"id": "manufactura", "label": "Manufactura"},
        {"id": "control", "label": "Control y robótica"},
        {"id": "integracion", "label": "Integración"},
        {"id": "gestion", "label": "Gestión"},
        {"id": "contexto", "label": "Contexto"},
        {"id": "libre", "label": "Libre"},
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
