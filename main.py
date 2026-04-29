from datetime import date

from modelo.libro import Libro
from modelo.estudiante import Estudiante
from modelo.profesor import Profesor
from modelo.biblioteca import Biblioteca
from modelo.generador import (
    generar_libros,
    generar_estudiantes,
    generar_profesores,
    generar_fecha_prestamo,
)


def separador(titulo: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {titulo}")
    print(f"{'─' * 60}")

def demo():

    biblioteca = Biblioteca("Biblioteca UNEMI")
    print(f"\n{biblioteca}")

    # Registrar libros (RF-01)
    separador("Generando 50 libros")
    libros = generar_libros(50)
    for libro in libros:
        biblioteca.registrar_libro(libro)

    # Registrar estudiantes (RF-02)
    separador("Generando 10 estudiantes")
    estudiantes = generar_estudiantes(10)
    for est in estudiantes:
        biblioteca.registrar_estudiante(est)

    # Registrar profesores (RF-07)
    separador("Generando 5 profesores")
    profesores = generar_profesores(5)
    for prof in profesores:
        biblioteca.registrar_profesor(prof)

    print(f"\n{biblioteca}")

    # Catálogo inicial (RF-09)
    separador("Catálogo generado (ordenado alfabéticamente)")
    biblioteca.mostrar_catalogo()

    # Préstamos a estudiantes (RF-03) 
    separador("Realizando préstamos aleatorios")

    prestamos_realizados = []
    for i, estudiante in enumerate(estudiantes[:3]):
        libro = libros[i]
        f_inicio, f_fin = generar_fecha_prestamo()
        resultado = biblioteca.prestar_libro(
            libro.isbn, estudiante.cedula, f_inicio, f_fin
        )
        print(resultado)
        if "✓" in resultado:
            prestamos_realizados.append((libro, estudiante, f_inicio, f_fin))

    # Préstamos a profesores (RF-08)
    prof = profesores[0]
    libro_prof = libros[3]
    f_inicio, f_fin = generar_fecha_prestamo()
    resultado = biblioteca.prestar_libro(
        libro_prof.isbn, prof.cedula, f_inicio, f_fin
    )
    print(resultado)

    # Validación libro ya prestado (RF-04)
    separador("Validación: intentando prestar libro ya prestado")
    if prestamos_realizados:
        libro_ocupado, _, _, _ = prestamos_realizados[0]
        otro_est = estudiantes[3]
        f_i, f_f = generar_fecha_prestamo()
        print(biblioteca.prestar_libro(
            libro_ocupado.isbn, otro_est.cedula, f_i, f_f
        ))

    # Préstamos activos del primer estudiante (RF-06)
    separador("Préstamos activos del primer estudiante")
    primer_est = estudiantes[0]
    print(f"  Consultando: {primer_est.nombre} {primer_est.apellido}")
    activos = biblioteca.consultar_prestamos_activos(primer_est.cedula)
    if activos:
        for p in activos:
            print(f"  → {p}")
    else:
        print("  (Sin préstamos activos)")

    # Devolución a tiempo (RF-10)
    separador("Devolución a tiempo (sin multa)")
    if prestamos_realizados:
        from datetime import datetime
        libro_dev, est_dev, _, f_fin = prestamos_realizados[0]
        fecha_limite = datetime.strptime(f_fin, "%Y-%m-%d").date()
        print(f"  Fecha límite : {fecha_limite}  |  Devuelve justo a tiempo")
        print(biblioteca.devolver_libro(
            libro_dev.isbn, est_dev.cedula, fecha_actual=fecha_limite
        ))

    # Devolución con retraso (RF-10)
    separador("Devolución con retraso (multa)")
    if len(prestamos_realizados) >= 2:
        from datetime import datetime, timedelta
        libro_ret, est_ret, _, f_fin2 = prestamos_realizados[1]
        fecha_limite2  = datetime.strptime(f_fin2, "%Y-%m-%d").date()
        dias_tarde     = 4
        fecha_dev_tard = fecha_limite2 + timedelta(days=dias_tarde)
        multa_esperada = dias_tarde * 0.50
        print(f"  Fecha límite : {fecha_limite2}  |  Devuelve: {fecha_dev_tard}")
        print(f"  Retraso esperado: {dias_tarde} días → Multa: ${multa_esperada:.2f}")
        print(biblioteca.devolver_libro(
            libro_ret.isbn, est_ret.cedula, fecha_actual=fecha_dev_tard
        ))

    # Catálogo final
    separador("Catálogo final tras préstamos y devoluciones")
    biblioteca.mostrar_catalogo()

    print(f"\n{'=' * 60}")
    print(f"  {biblioteca}")
    print(f"{'=' * 60}")


# ══════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════

def main():
    demo()  


if __name__ == "__main__":
    main()
