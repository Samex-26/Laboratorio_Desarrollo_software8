"""Utilidades de entrada/salida con manejo de errores centralizado."""

import csv
import json
from functools import wraps


def manejarErroresArchivo(func):
    """Decorador que captura errores comunes de archivos y los relanza en español.

    Captura:
        - FileNotFoundError: cuando el archivo no existe.
        - PermissionError: cuando no hay permisos para acceder al archivo.
        - json.JSONDecodeError: cuando el contenido JSON es inválido.
        - csv.Error: cuando el contenido CSV es inválido.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"No se encontró el archivo solicitado: '{error.filename}'. "
                "Verifique la ruta e intente nuevamente."
            ) from error
        except PermissionError as error:
            raise PermissionError(
                f"No hay permisos para acceder al archivo: '{error.filename}'. "
                "Cierre el archivo si está en uso o revise los permisos."
            ) from error
        except json.JSONDecodeError as error:
            raise json.JSONDecodeError(
                f"El contenido JSON es inválido: {error.msg} "
                f"(línea {error.lineno}, columna {error.colno}).",
                error.doc,
                error.pos,
            ) from error
        except csv.Error as error:
            raise csv.Error(
                f"El contenido CSV es inválido: {error}. "
                "Revise el formato, delimitadores y comillas del archivo."
            ) from error

    return wrapper
