class Libro:
    """Representa un libro del catálogo de la biblioteca."""

    def __init__(self, isbn: str, titulo: str, autor: str):
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._disponible = True

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