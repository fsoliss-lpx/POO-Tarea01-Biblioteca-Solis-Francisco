# modelo/generador.py
"""
Módulo para generar datos aleatorios usando la librería Faker.
Genera objetos Libro, Estudiante y Profesor con datos ficticios pero realistas.

Instalación previa requerida:
    pip install faker
"""

import random
from faker import Faker

from modelo.libro import Libro
from modelo.estudiante import Estudiante
from modelo.profesor import Profesor

# Faker en español latinoamericano
fake = Faker("es_MX")

# ── Datos temáticos fijos ──────────────────────────────────────────────────────

CARRERAS = [
    "Ingeniería en Software",
    "Ingeniería Industrial",
    "Ingeniería Civil",
    "Administración de Empresas",
    "Contabilidad y Auditoría",
    "Medicina",
    "Derecho",
    "Psicología",
    "Arquitectura",
    "Diseño Gráfico",
]

DEPARTAMENTOS = [
    "Ciencias de la Computación",
    "Matemáticas y Física",
    "Ciencias Sociales",
    "Ciencias Económicas",
    "Ciencias de la Salud",
    "Humanidades y Letras",
    "Arquitectura y Diseño",
]

TITULOS_LIBROS = [
    ("Fundamentos de Programación",        "Carlos Méndez"),
    ("Cálculo Diferencial e Integral",     "James Stewart"),
    ("Introducción a la Economía",         "N. Gregory Mankiw"),
    ("Derecho Civil Aplicado",             "Eugenia Ariano"),
    ("Psicología del Comportamiento",      "David Myers"),
    ("Bases de Datos Relacionales",        "Ramez Elmasri"),
    ("Algoritmos y Estructuras de Datos",  "Thomas H. Cormen"),
    ("Física Universitaria",               "Hugh Young"),
    ("Química General",                    "Raymond Chang"),
    ("Anatomía Humana",                    "Frank Netter"),
    ("Historia del Arte",                  "Ernst Gombrich"),
    ("Gestión de Proyectos",               "Harold Kerzner"),
    ("Redes de Computadoras",              "Andrew Tanenbaum"),
    ("Estadística para Administración",    "Richard Levin"),
    ("Biología Celular y Molecular",       "Harvey Lodish"),
    ("Termodinámica Aplicada",             "Yunus Çengel"),
    ("Marketing Digital",                  "Philip Kotler"),
    ("Ética Profesional",                  "Manuel Velásquez"),
    ("Sistemas Operativos Modernos",       "Andrew Tanenbaum"),
    ("Inteligencia Artificial",            "Stuart Russell"),
]

"""Genera un ISBN-13 con formato real (sin validación de dígito de control)."""
def _generar_isbn() -> str:

    grupo = random.choice(["978", "979"])
    editorial = str(random.randint(10, 99))
    titulo_num = str(random.randint(10000, 99999))
    control = str(random.randint(0, 9))
    return f"{grupo}-{editorial}-{titulo_num}-{control}"

"""Genera una cédula ecuatoriana ficticia de 10 dígitos."""
def _generar_cedula() -> str:
    provincia = str(random.randint(1, 24)).zfill(2)
    resto = str(random.randint(1000000, 9999999))
    return f"{provincia}{resto}"

# Generadores públicos

"""Retorna un objeto Libro con datos aleatorios."""
def generar_libro() -> Libro:
    titulo, autor = random.choice(TITULOS_LIBROS)
    # Agrega un sufijo aleatorio para evitar títulos duplicados
    sufijo = fake.bothify(text="Vol. ?#")
    isbn = _generar_isbn()
    return Libro(isbn, f"{titulo} — {sufijo}", autor)

"""Retorna una lista de `cantidad` objetos Libro aleatorios."""
def generar_libros(cantidad: int) -> list:
    return [generar_libro() for _ in range(cantidad)]

"""Retorna un objeto Estudiante con datos aleatorios."""
def generar_estudiante() -> Estudiante:
    nombre   = fake.first_name()
    apellido = fake.last_name()
    cedula   = _generar_cedula()
    carrera  = random.choice(CARRERAS)
    return Estudiante(cedula, nombre, apellido, carrera)

"""Retorna una lista de `cantidad` objetos Estudiante aleatorios."""
def generar_estudiantes(cantidad: int) -> list:
    return [generar_estudiante() for _ in range(cantidad)]

"""Retorna un objeto Profesor con datos aleatorios."""
def generar_profesor() -> Profesor:
    # Los profesores llevan título académico
    titulo   = random.choice(["Dr.", "Dra.", "Mg.", "Ing.", "Lic."])
    nombre   = f"{titulo} {fake.first_name()}"
    apellido = fake.last_name()
    cedula   = _generar_cedula()
    depto    = random.choice(DEPARTAMENTOS)
    return Profesor(cedula, nombre, apellido, depto)

"""Retorna una lista de `cantidad` objetos Profesor aleatorios."""
def generar_profesores(cantidad: int) -> list:
    return [generar_profesor() for _ in range(cantidad)]

"""
Retorna una tupla (fecha_prestamo, fecha_devolucion) como strings.
El préstamo es en abril 2026 y el plazo es de entre 7 y 21 días.
"""
def generar_fecha_prestamo() -> tuple:
   
    from datetime import date, timedelta
    inicio = date(2026, 4, 1)
    fin    = date(2026, 4, 20)
    delta  = (fin - inicio).days
    fecha_prestamo    = inicio + timedelta(days=random.randint(0, delta))
    fecha_devolucion  = fecha_prestamo + timedelta(days=random.randint(7, 21))
    return (
        fecha_prestamo.strftime("%Y-%m-%d"),
        fecha_devolucion.strftime("%Y-%m-%d"),
    )