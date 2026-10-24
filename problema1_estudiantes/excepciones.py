class ErrorEstudiante(Exception):
    """Excepción base para cualquier error del dominio de estudiantes."""


class ArchivoEstudiantesError(ErrorEstudiante):
    """Error relacionado con el archivo de estudiantes o su estructura."""


class RegistroInvalidoError(ErrorEstudiante):
    """Una fila del CSV no cumple el formato o el contenido esperado."""


class NotaFueraDeRangoError(RegistroInvalidoError):
    """Una nota está fuera del rango permitido (0-100)."""


class CedulaDuplicadaError(RegistroInvalidoError):
    """Se encontró una cédula repetida dentro del archivo."""
