class ErrorInventario(Exception):
    """Excepción base para cualquier error del dominio de inventario."""


class ArchivoInventarioError(ErrorInventario):
    """Error relacionado con el archivo de inventario o su estructura."""


class ProductoInvalidoError(ErrorInventario):
    """Un producto del archivo no cumple el formato o el contenido esperado."""


class CodigoDuplicadoError(ProductoInvalidoError):
    """Se encontró un código de producto repetido."""


class ProductoNoEncontradoError(ErrorInventario):
    """No existe un producto con el código solicitado."""


class MovimientoInvalidoError(ErrorInventario):
    """Un movimiento (entrada/salida) tiene datos inválidos."""


class ExistenciaInsuficienteError(MovimientoInvalidoError):
    """Una salida dejaría la existencia del producto en negativo."""
