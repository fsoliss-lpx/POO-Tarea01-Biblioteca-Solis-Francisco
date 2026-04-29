## Ingieneria en Software-4TO Semestre
## Integrantes
1. FRANCISCO XAVIER SOLIS SANTILLAN
2. JORGE ALFREDO PATIÑO SUAREZ
3. ALLISON LIZBETH OLEA NUÑEZ
4. LUIS EDUARDO FREIRE BRAVO
5. MIGUEL JOSE VELASTEGUI PALACIOS
# Sistema de Gestión de Biblioteca Universitaria
> La **Biblioteca Central de la UNEMI** necesita un sistema básico para gestionar el préstamo de libros a estudiantes. Actualmente, todo se realiza de forma manual en cuadernos y hojas de registro, lo que provoca pérdida de información, préstamos duplicados y libros extraviados.
>
> El sistema debe permitir **registrar libros** con su título, autor, número ISBN y estado de disponibilidad. También debe permitir **registrar estudiantes** con su cédula, nombre, apellido y carrera universitaria.
>
> Cuando un estudiante solicita un libro, se genera un **préstamo** que registra la fecha del préstamo, la fecha límite de devolución y el estado del préstamo (activo o devuelto). Un estudiante puede tener **varios préstamos activos**, pero un libro solo puede estar prestado a **un estudiante a la vez**.
>
> La biblioteca necesita poder **consultar los préstamos activos** de un estudiante, **registrar la devolución** de un libro y **verificar la disponibilidad** de un libro antes de prestarlo.
### Requerimientos Funcionales

A partir del análisis anterior, formalizamos los requerimientos:
| ID | Requerimiento | Prioridad |
|----|--------------|-----------|
| RF-01 | El sistema debe permitir registrar libros con título, autor, ISBN y disponibilidad | Alta |
| RF-02 | El sistema debe permitir registrar estudiantes con cédula, nombre, apellido y carrera | Alta |
| RF-03 | El sistema debe permitir registrar un préstamo asociando un usuario con un libro | Alta |
| RF-04 | El sistema debe validar que un libro esté disponible antes de prestarlo | Alta |
| RF-05 | El sistema debe permitir registrar la devolución de un libro | Alta |
| RF-06 | El sistema debe permitir consultar los préstamos activos de un usuario | Media |
| RF-07 | El sistema debe permitir registrar profesores con cédula, nombre, apellido y departamento | Alta |
| RF-08 | El sistema debe permitir prestar libros tanto a estudiantes como a profesores | Alta |
| RF-09 | El sistema debe mostrar el catálogo de libros ordenado alfabéticamente con su estado | Media |
| RF-10 | El sistema debe calcular una multa de $0.50 por día si la devolución es tardía | Alta |
### Analisis
#### Tabla de Abstracción 

**Entidad 1: Persona** (clase base)

| Aspecto | Detalle |
|---------|---------|
| **Atributos esenciales** | cédula, nombre, apellido |
| **Comportamientos** | Mostrar información personal (`__str__`) |
| **¿Qué descarto?** | Dirección, teléfono, fecha de nacimiento, foto — no son necesarios para el sistema de biblioteca |

**Entidad 2: Estudiante** (hereda de Persona)

| Aspecto | Detalle |
|---------|---------|
| **Atributos esenciales** | carrera (hereda: cédula, nombre, apellido) |
| **Comportamientos** | Mostrar información completa incluyendo carrera |
| **¿Qué descarto?** | Semestre, promedio, materias inscritas — no son relevantes para préstamos |

**Entidad 3: Profesor** (hereda de Persona) ← *nuevo*

| Aspecto | Detalle |
|---------|---------|
| **Atributos esenciales** | departamento (hereda: cédula, nombre, apellido) |
| **Comportamientos** | Mostrar información completa incluyendo departamento |
| **¿Qué descarto?** | Título académico, materias que dicta, horario — fuera del alcance del sistema |

**Entidad 4: Libro**

| Aspecto | Detalle |
|---------|---------|
| **Atributos esenciales** | isbn, titulo, autor, disponible (bool) |
| **Comportamientos** | Verificar disponibilidad, marcar como prestado, marcar como devuelto, mostrar información |
| **¿Qué descarto?** | Número de páginas, editorial, año de publicación, ubicación en estante — no son necesarios para el préstamo |

**Entidad 5: Préstamo**

| Aspecto | Detalle |
|---------|---------|
| **Atributos esenciales** | libro, usuario (Persona), fecha_prestamo, fecha_devolucion, activo (bool), multa (float) |
| **Comportamientos** | Registrar devolución con cálculo de multa por retraso, mostrar información del préstamo |
| **¿Qué descarto?** | Renovaciones, observaciones — complejidad que no necesitamos en este caso |

**Entidad 6: Biblioteca**

| Aspecto | Detalle |
|---------|---------|
| **Atributos esenciales** | nombre, lista de libros, lista de estudiantes, lista de profesores, lista de préstamos |
| **Comportamientos** | Registrar libro, registrar estudiante, registrar profesor, prestar libro, devolver libro (con multa), consultar préstamos activos, mostrar catálogo |
| **¿Qué descarto?** | Horarios, ubicación física, personal administrativo — fuera del alcance |
### Relaciones

| Relación | Tipo | Justificación |
|----------|------|---------------|
| `Estudiante` **es un** `Persona` | **Herencia** | Un estudiante es un tipo especial de persona con atributo adicional (carrera) |
| `Profesor` **es un** `Persona` | **Herencia** | Un profesor es un tipo especial de persona con atributo adicional (departamento) |
| `Préstamo` **contiene un** `Libro` | **Asociación** | Un préstamo referencia a un libro, pero el libro existe independientemente del préstamo |
| `Préstamo` **contiene un** `Persona` | **Asociación** | Un préstamo referencia a un usuario (Estudiante o Profesor), que existe independientemente |
| `Biblioteca` **tiene muchos** `Libro` | **Composición** | La biblioteca gestiona sus libros; si la biblioteca se elimina, sus registros de libros también |
| `Biblioteca` **tiene muchos** `Estudiante` | **Agregación** | La biblioteca registra estudiantes, pero los estudiantes existen fuera de la biblioteca |
| `Biblioteca` **tiene muchos** `Profesor` | **Agregación** | La biblioteca registra profesores, pero los profesores existen fuera de la biblioteca |
| `Biblioteca` **tiene muchos** `Préstamo` | **Composición** | Los préstamos son gestionados por la biblioteca |
#### Diseño
#### Clases individuales
En este apartado veremos el diseño de las clases individuales, dentro del archivo en la carpeta de diagrama veremos el archivo biblioteca.puml donde veremos el diagrama UML con las clases, relaciones y cardinalidad.
**Clase `Persona`**:
```
┌──────────────────────────────┐
│          Persona              │
├──────────────────────────────┤
│ - _cedula: str                │
│ - _nombre: str                │
│ - _apellido: str              │
├──────────────────────────────┤
│ + cedula: str  {property}     │
│ + nombre: str  {property}     │
│ + apellido: str  {property}   │
│ + __str__(): str              │
└──────────────────────────────┘
```

**Clase `Estudiante`**:
```
┌──────────────────────────────┐
│         Estudiante            │
├──────────────────────────────┤
│ - _carrera: str               │
├──────────────────────────────┤
│ + carrera: str  {property}    │
│ + __str__(): str              │
└──────────────────────────────┘
```

**Clase `Profesor`**:
```
┌──────────────────────────────────┐
│            Profesor               │
├──────────────────────────────────┤
│ - _departamento: str              │
├──────────────────────────────────┤
│ + departamento: str  {property}   │
│ + __str__(): str                  │
└──────────────────────────────────┘
```

**Clase `Libro`**:
```
┌──────────────────────────────────┐
│             Libro                 │
├──────────────────────────────────┤
│ - _isbn: str                      │
│ - _titulo: str                    │
│ - _autor: str                     │
│ - _disponible: bool               │
├──────────────────────────────────┤
│ + isbn: str  {property}           │
│ + titulo: str  {property}         │
│ + autor: str  {property}          │
│ + disponible: bool  {property}    │
│ + prestar(): None                 │
│ + devolver(): None                │
│ + __str__(): str                  │
└──────────────────────────────────┘
```

**Clase `Prestamo`**:
```
┌────────────────────────────────────────────┐
│                 Prestamo                    │
├────────────────────────────────────────────┤
│ + MULTA_POR_DIA: float = 0.50              │
│ - _libro: Libro                             │
│ - _usuario: Persona                         │
│ - _fecha_prestamo_str: str                  │
│ - _fecha_devolucion_str: str                │
│ - _fecha_devolucion: date                   │
│ - _activo: bool                             │
│ - _multa: float                             │
├────────────────────────────────────────────┤
│ + libro: Libro  {property}                  │
│ + usuario: Persona  {property}              │
│ + activo: bool  {property}                  │
│ + multa: float  {property}                  │
│ + registrar_devolucion(fecha: date): dict   │
│ + __str__(): str                            │
└────────────────────────────────────────────┘
```

**Clase `Biblioteca`**:
```
┌──────────────────────────────────────────────────────────────┐
│                         Biblioteca                            │
├──────────────────────────────────────────────────────────────┤
│ - _nombre: str                                                │
│ - _libros: list[Libro]                                        │
│ - _estudiantes: list[Estudiante]                              │
│ - _profesores: list[Profesor]                                 │
│ - _prestamos: list[Prestamo]                                  │
├──────────────────────────────────────────────────────────────┤
│ + registrar_libro(libro: Libro): None                         │
│ + registrar_estudiante(estudiante: Estudiante): None          │
│ + registrar_profesor(profesor: Profesor): None                │
│ - _buscar_libro(isbn: str): Libro                             │
│ - _buscar_usuario(cedula: str): Persona                       │
│ + prestar_libro(isbn, cedula, fecha, fecha_dev): str          │
│ + devolver_libro(isbn, cedula, fecha_actual: date): str       │
│ + consultar_prestamos_activos(cedula: str): list              │
│ + mostrar_catalogo(): None                                    │
│ + __str__(): str                                              │
└──────────────────────────────────────────────────────────────┘
```
### Desarrollo
### Estructura de Archivos a Crear

Crea la siguiente estructura de carpetas y archivos:

```
biblioteca/
├── modelo/
│   ├── __init__.py
│   ├── persona.py
│   ├── estudiante.py
│   ├── profesor.py
│   ├── libro.py
│   ├── prestamo.py
│   └── biblioteca.py
└── main.py
```
El **__init__.py** vacío le dice a Python que la carpeta modelo/ es un paquete, no una carpeta normal. Sin ese archivo, Python no reconoce la carpeta como paquete y los imports **modelo.xxx** los reconoceria como error.
---
#### Clase 1: `persona.py` — La clase base
```
class Persona:

    def __init__(self, cedula: str, nombre: str, apellido: str):
        self._cedula = cedula
        self._nombre = nombre
        self._apellido = apellido

    @property
    def cedula(self) -> str:
        return self._cedula

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellido(self) -> str:
        return self._apellido

    def __str__(self) -> str:
        return f"{self._cedula}: {self._nombre} {self._apellido}"
```

**Explicación línea por línea:**
- `class Persona:` → Define la clase (del rectángulo superior del UML).
- `def __init__(self, ...)` → Constructor que inicializa los atributos privados.
- `self._cedula` → El guion bajo `_` indica atributo privado (convención Python = `-` en UML).
- `@property` → Permite acceder al atributo como si fuera público: `persona.cedula` en vez de `persona.get_cedula()`.
- `__str__` → Método especial para representación legible del objeto.

---

#### Clase 2: `estudiante.py` 

```python
# modelo/estudiante.py

from modelo.persona import Persona


class Estudiante(Persona):
    """Estudiante universitario. Hereda de Persona."""

    def __init__(self, cedula: str, nombre: str, apellido: str, carrera: str):
        super().__init__(cedula, nombre, apellido)
        self._carrera = carrera

    @property
    def carrera(self) -> str:
        return self._carrera

    def __str__(self) -> str:
        return f"{super().__str__()} | Carrera: {self._carrera}"
```

**Puntos clave:**
- `class Estudiante(Persona)` → La herencia del UML (`Estudiante ──▷ Persona`).
- `super().__init__(...)` → Llama al constructor de `Persona` para inicializar cédula, nombre y apellido. **No duplicamos código**.
- `super().__str__()` → Reutiliza la representación de `Persona` y le agrega la carrera.

---

#### Clase 3: `profesor.py` — Segunda clase hija 

```python
# modelo/profesor.py

from modelo.persona import Persona


class Profesor(Persona):
    """Profesor universitario. Hereda de Persona."""

    def __init__(self, cedula: str, nombre: str, apellido: str, departamento: str):
        super().__init__(cedula, nombre, apellido)
        self._departamento = departamento

    @property
    def departamento(self) -> str:
        return self._departamento

    def __str__(self) -> str:
        return f"{super().__str__()} | Departamento: {self._departamento}"
```

**Puntos clave:**
- Sigue exactamente el mismo patrón de herencia que `Estudiante`.
- Solo agrega el atributo propio (`_departamento`) sin duplicar cédula, nombre ni apellido.
- Ambas clases (`Estudiante` y `Profesor`) son **polimórficas** respecto a `Persona`.

---

#### Clase 4: `libro.py`
```python
# modelo/libro.py

class Libro:
    """Representa un libro de la biblioteca."""

    def __init__(self, isbn: str, titulo: str, autor: str):
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._disponible = True  # Por defecto, un libro nuevo está disponible

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def autor(self) -> str:
        return self._autor

    @property
    def disponible(self) -> bool:
        return self._disponible

    def prestar(self) -> None:
        """Marca el libro como no disponible."""
        self._disponible = False

    def devolver(self) -> None:
        """Marca el libro como disponible."""
        self._disponible = True

    def __str__(self) -> str:
        estado = "Disponible" if self._disponible else "Prestado"
        return f"[{self._isbn}] {self._titulo} - {self._autor} ({estado})"
```

**Puntos clave:**
- `_disponible = True` → Valor por defecto, no se pide en el constructor.
- `prestar()` y `devolver()` → Métodos que **controlan el acceso** al estado interno. El código externo no puede hacer `libro._disponible = False` directamente. Esto es **encapsulamiento**.

---

#### Clase 5: `prestamo.py` 

```python
# modelo/prestamo.py

from datetime import date, datetime

from modelo.libro import Libro
from modelo.persona import Persona
from modelo.profesor import Profesor


class Prestamo:
    """Representa un préstamo de un libro a un usuario (Estudiante o Profesor)."""

    MULTA_POR_DIA = 0.50  # dólares

    def __init__(self, libro: Libro, usuario: Persona,
                 fecha_prestamo: str, fecha_devolucion: str):
        self._libro = libro
        self._usuario = usuario
        self._fecha_prestamo_str = fecha_prestamo
        self._fecha_devolucion_str = fecha_devolucion
        self._fecha_devolucion = datetime.strptime(fecha_devolucion, "%Y-%m-%d").date()
        self._activo = True
        self._multa = 0.0

    @property
    def libro(self) -> Libro:
        return self._libro

    @property
    def usuario(self) -> Persona:
        return self._usuario

    # Alias para compatibilidad con código que use .estudiante
    @property
    def estudiante(self) -> Persona:
        return self._usuario

    @property
    def activo(self) -> bool:
        return self._activo

    @property
    def multa(self) -> float:
        return self._multa

    def registrar_devolucion(self, fecha_actual: date = None) -> dict:
        """
        Marca el préstamo como devuelto y libera el libro.
        Calcula multa de $0.50 por día si hay retraso.
        Retorna dict con: dias_retraso, multa.
        """
        if fecha_actual is None:
            fecha_actual = date.today()

        self._activo = False
        self._libro.devolver()

        dias_retraso = (fecha_actual - self._fecha_devolucion).days
        if dias_retraso > 0:
            self._multa = dias_retraso * self.MULTA_POR_DIA
        else:
            dias_retraso = 0
            self._multa = 0.0

        return {"dias_retraso": dias_retraso, "multa": self._multa}

    def __str__(self) -> str:
        estado = "ACTIVO" if self._activo else "DEVUELTO"
        tipo = "Prof." if isinstance(self._usuario, Profesor) else "Est."
        base = (f"Préstamo [{estado}]: {self._libro.titulo} → "
                f"{tipo} {self._usuario.nombre} {self._usuario.apellido} | "
                f"Desde: {self._fecha_prestamo_str} | "
                f"Hasta: {self._fecha_devolucion_str}")
        if self._multa > 0:
            base += f" | Multa: ${self._multa:.2f}"
        return base
```

**Puntos clave:**
- `self._usuario = usuario` → Ahora acepta cualquier `Persona` (Estudiante **o** Profesor). Esto es **polimorfismo**.
- `_fecha_devolucion` se guarda como objeto `date` para poder calcular diferencias de días.
- `registrar_devolucion()` retorna un `dict` con el retraso y la multa calculada.
- `isinstance(self._usuario, Profesor)` → Permite diferenciar el tipo de usuario en el `__str__`.

---

#### Clase 6: `biblioteca.py`

```python
# modelo/biblioteca.py

from datetime import date

from modelo.libro import Libro
from modelo.estudiante import Estudiante
from modelo.profesor import Profesor
from modelo.persona import Persona
from modelo.prestamo import Prestamo


class Biblioteca:
    """Gestiona libros, estudiantes, profesores y préstamos."""

    def __init__(self, nombre: str):
        self._nombre = nombre
        self._libros = []
        self._estudiantes = []
        self._profesores = []
        self._prestamos = []

    def registrar_libro(self, libro: Libro) -> None:
        """Agrega un libro al catálogo de la biblioteca."""
        self._libros.append(libro)
        print(f"  ✓ Libro registrado: {libro.titulo}")

    def registrar_estudiante(self, estudiante: Estudiante) -> None:
        """Registra un estudiante en la biblioteca."""
        self._estudiantes.append(estudiante)
        print(f"  ✓ Estudiante registrado: {estudiante.nombre} {estudiante.apellido}")

    def registrar_profesor(self, profesor: Profesor) -> None:
        """Registra un profesor en la biblioteca."""
        self._profesores.append(profesor)
        print(f"  ✓ Profesor registrado: {profesor.nombre} {profesor.apellido} "
              f"[{profesor.departamento}]")

    def _buscar_libro(self, isbn: str) -> Libro:
        """Busca un libro por ISBN. Retorna None si no existe."""
        for libro in self._libros:
            if libro.isbn == isbn:
                return libro
        return None

    def _buscar_usuario(self, cedula: str) -> Persona:
        """Busca por cédula en estudiantes y profesores."""
        for est in self._estudiantes:
            if est.cedula == cedula:
                return est
        for prof in self._profesores:
            if prof.cedula == cedula:
                return prof
        return None

    def prestar_libro(self, isbn: str, cedula: str,
                      fecha_prestamo: str, fecha_devolucion: str) -> str:
        """Registra un préstamo si el libro está disponible.
        Funciona tanto para Estudiantes como para Profesores."""
        libro = self._buscar_libro(isbn)
        if libro is None:
            return f"  ✗ Error: No se encontró el libro con ISBN {isbn}"

        usuario = self._buscar_usuario(cedula)
        if usuario is None:
            return f"  ✗ Error: No se encontró usuario con cédula {cedula}"

        if not libro.disponible:
            return f"  ✗ Error: El libro '{libro.titulo}' no está disponible"

        libro.prestar()
        prestamo = Prestamo(libro, usuario, fecha_prestamo, fecha_devolucion)
        self._prestamos.append(prestamo)
        tipo = "Profesor" if isinstance(usuario, Profesor) else "Estudiante"
        return (f"  ✓ Préstamo registrado: '{libro.titulo}' → "
                f"{tipo} {usuario.nombre} {usuario.apellido}")

    def devolver_libro(self, isbn: str, cedula: str,
                       fecha_actual: date = None) -> str:
        """
        Registra la devolución de un libro.
        Si hay retraso, calcula multa de $0.50 por día.
        fecha_actual: permite simular fechas para pruebas (default = hoy).
        """
        if fecha_actual is None:
            fecha_actual = date.today()

        for prestamo in self._prestamos:
            if (prestamo.libro.isbn == isbn and
                    prestamo.usuario.cedula == cedula and
                    prestamo.activo):

                resultado = prestamo.registrar_devolucion(fecha_actual)
                msg = f"  ✓ Devolución registrada: '{prestamo.libro.titulo}'"

                if resultado["dias_retraso"] > 0:
                    msg += (f"\n  ⚠ Retraso: {resultado['dias_retraso']} día(s) → "
                            f"Multa: ${resultado['multa']:.2f}")
                else:
                    msg += "\n  ✓ Devuelto a tiempo. Sin multa."
                return msg

        return "  ✗ Error: No se encontró un préstamo activo con esos datos"

    def consultar_prestamos_activos(self, cedula: str) -> list:
        """Retorna los préstamos activos de un usuario."""
        return [p for p in self._prestamos
                if p.usuario.cedula == cedula and p.activo]

    def mostrar_catalogo(self) -> None:
        """Muestra todos los libros ordenados alfabéticamente por título."""
        print(f"\n  {'─' * 52}")
        print(f"  CATÁLOGO — {self._nombre}")
        print(f"  {'─' * 52}")
        if not self._libros:
            print("  (Sin libros registrados)")
            return
        libros_ordenados = sorted(self._libros, key=lambda l: l.titulo.lower())
        for i, libro in enumerate(libros_ordenados, 1):
            estado = "🟢 Disponible" if libro.disponible else "🔴 Prestado  "
            print(f"  {i:2}. {estado} | {libro.titulo} — {libro.autor}")
        print(f"  {'─' * 52}")
        total = len(self._libros)
        disponibles = sum(1 for l in self._libros if l.disponible)
        print(f"  Total: {total} libro(s) | Disponibles: {disponibles} | "
              f"Prestados: {total - disponibles}")

    def __str__(self) -> str:
        total_usuarios = len(self._estudiantes) + len(self._profesores)
        return (f"Biblioteca '{self._nombre}' | "
                f"Libros: {len(self._libros)} | "
                f"Usuarios: {total_usuarios} "
                f"(Est: {len(self._estudiantes)}, Prof: {len(self._profesores)}) | "
                f"Préstamos: {len(self._prestamos)}")
```

**Puntos clave:**
- `_buscar_usuario()` reemplaza a `_buscar_estudiante()` y busca en **ambas** listas. Es privado (`_`) porque solo la biblioteca lo usa internamente.
- `prestar_libro()` funciona sin cambios para Estudiantes y Profesores gracias al polimorfismo.
- `mostrar_catalogo()` usa `sorted()` con `key=lambda` para ordenar ignorando mayúsculas/minúsculas.
- `devolver_libro()` acepta `fecha_actual` como parámetro para facilitar pruebas con fechas simuladas.