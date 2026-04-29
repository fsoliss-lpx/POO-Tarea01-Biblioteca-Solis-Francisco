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
        Calcula multa de $0.50 por día si hay retraso. (Nivel 3)
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