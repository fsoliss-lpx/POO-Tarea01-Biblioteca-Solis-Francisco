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
        self._profesores = []   # Nivel 1
        self._prestamos = []

    # ── Registro ──────────────────────────────────────────────

    def registrar_libro(self, libro: Libro) -> None:
        """Agrega un libro al catálogo de la biblioteca."""
        self._libros.append(libro)
        print(f"  ✓ Libro registrado: {libro.titulo}")

    def registrar_estudiante(self, estudiante: Estudiante) -> None:
        """Registra un estudiante en la biblioteca."""
        self._estudiantes.append(estudiante)
        print(f"  ✓ Estudiante registrado: {estudiante.nombre} {estudiante.apellido}")

    def registrar_profesor(self, profesor: Profesor) -> None:
        """Registra un profesor en la biblioteca. (Nivel 1)"""
        self._profesores.append(profesor)
        print(f"  ✓ Profesor registrado: {profesor.nombre} {profesor.apellido} "
              f"[{profesor.departamento}]")

    # ── Búsquedas internas ────────────────────────────────────

    def _buscar_libro(self, isbn: str) -> Libro:
        """Busca un libro por ISBN. Retorna None si no existe."""
        for libro in self._libros:
            if libro.isbn == isbn:
                return libro
        return None

    def _buscar_usuario(self, cedula: str) -> Persona:
        """Busca por cédula en estudiantes y profesores. (Nivel 1)"""
        for est in self._estudiantes:
            if est.cedula == cedula:
                return est
        for prof in self._profesores:
            if prof.cedula == cedula:
                return prof
        return None

    # ── Préstamo ──────────────────────────────────────────────

    def prestar_libro(self, isbn: str, cedula: str,
                      fecha_prestamo: str, fecha_devolucion: str) -> str:
        """Registra un préstamo si el libro está disponible.
        Funciona tanto para Estudiantes como para Profesores. (Nivel 1)"""
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

    # ── Devolución ────────────────────────────────────────────

    def devolver_libro(self, isbn: str, cedula: str,
                       fecha_actual: date = None) -> str:
        """
        Registra la devolución de un libro.
        Si hay retraso, calcula multa de $0.50 por día. (Nivel 3)
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

    # ── Consultas ─────────────────────────────────────────────

    def consultar_prestamos_activos(self, cedula: str) -> list:
        """Retorna los préstamos activos de un usuario."""
        return [p for p in self._prestamos
                if p.usuario.cedula == cedula and p.activo]

    def mostrar_catalogo(self) -> None:
        """Muestra todos los libros ordenados alfabéticamente por título. (Nivel 2)"""
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
        