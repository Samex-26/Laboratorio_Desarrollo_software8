PESO_PARCIAL1 = 0.30
PESO_PARCIAL2 = 0.30
PESO_PROYECTO = 0.40
NOTA_MINIMA_APROBACION = 71


class Estudiante:

    def __init__(self, cedula, nombre, parcial1, parcial2, proyecto):
        self.cedula = cedula
        self.nombre = nombre
        self.parcial1 = parcial1
        self.parcial2 = parcial2
        self.proyecto = proyecto
        self.notaFinal = None
        self.condicion = None

    def calcularNotaFinal(self):
        """Calcula la nota final con pesos 30/30/40 y la asigna al objeto."""
        self.notaFinal = round(
            self.parcial1 * PESO_PARCIAL1
            + self.parcial2 * PESO_PARCIAL2
            + self.proyecto * PESO_PROYECTO,
            2,
        )
        return self.notaFinal

    def clasificar(self):
        self.condicion = (
            "APROBADO"
            if self.notaFinal >= NOTA_MINIMA_APROBACION
            else "REPROBADO"
        )
        return self.condicion

    def aDict(self):
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "parcial1": self.parcial1,
            "parcial2": self.parcial2,
            "proyecto": self.proyecto,
            "nota_final": self.notaFinal,
            "condicion": self.condicion,
        }

    def __repr__(self):
        return (
            f"Estudiante(cedula={self.cedula!r}, nombre={self.nombre!r}, "
            f"nota_final={self.notaFinal!r}, condicion={self.condicion!r})"
        )
