import csv
import json

from common.io_utils import manejarErroresArchivo
from common.validadores import validarNoVacio, validarRangoNumerico

from problema2_inventario.excepciones import (
    ArchivoInventarioError,
    CodigoDuplicadoError,
    ExistenciaInsuficienteError,
    MovimientoInvalidoError,
    ProductoInvalidoError,
    ProductoNoEncontradoError,
)
from problema2_inventario.modelos import Movimiento, Producto

CAMPOS_REQUERIDOS = ("codigo", "producto", "cantidad", "precio")
TIPOS_MOVIMIENTO = ("entrada", "salida")
MINIMO_PRODUCTOS = 20
CANTIDAD_MAXIMA = 1_000_000
PRECIO_MAXIMO = 1_000_000
UMBRAL_BAJO_STOCK = 15


class GestorInventario:

    def __init__(self):
        self.productos = {}
        self.movimientos = []

    @manejarErroresArchivo
    def cargarJson(self, ruta):
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ArchivoInventarioError(
                f"El archivo '{ruta}' debe contener una lista JSON de productos."
            )
        for indice, item in enumerate(datos, start=1):
            self._procesarProducto(item, indice)

        if len(self.productos) < MINIMO_PRODUCTOS:
            raise ArchivoInventarioError(
                f"El inventario debe contener al menos {MINIMO_PRODUCTOS} "
                f"productos válidos; se encontraron {len(self.productos)}."
            )
        return self.listar()

    def _procesarProducto(self, item, indice):
        if not isinstance(item, dict):
            raise ProductoInvalidoError(
                f"Producto #{indice}: se esperaba un objeto JSON con los "
                f"campos {CAMPOS_REQUERIDOS}."
            )
        for campo in CAMPOS_REQUERIDOS:
            try:
                validarNoVacio(item.get(campo), campo)
            except ValueError as error:
                raise ProductoInvalidoError(
                    f"Producto #{indice}: {error}"
                ) from error

        codigo = str(item["codigo"]).strip()
        nombre = str(item["producto"]).strip()
        cantidad = self._validarNumero(
            item["cantidad"], "cantidad", 0, CANTIDAD_MAXIMA, indice
        )
        if not float(cantidad).is_integer():
            raise ProductoInvalidoError(
                f"Producto #{indice}: la cantidad '{item['cantidad']}' debe "
                "ser un número entero."
            )
        precio = self._validarNumero(
            item["precio"], "precio", 0, PRECIO_MAXIMO, indice
        )

        if codigo in self.productos:
            raise CodigoDuplicadoError(
                f"Producto #{indice}: el código '{codigo}' está duplicado."
            )
        self.productos[codigo] = Producto(codigo, nombre, int(cantidad), precio)

    @staticmethod
    def _validarNumero(valor, campo, minimo, maximo, indice):
        try:
            numero = float(valor)
        except (TypeError, ValueError) as error:
            raise ProductoInvalidoError(
                f"Producto #{indice}: el campo '{campo}' ('{valor}') no es numérico."
            ) from error
        try:
            validarRangoNumerico(numero, minimo, maximo)
        except (TypeError, ValueError) as error:
            raise ProductoInvalidoError(
                f"Producto #{indice}: {error}"
            ) from error
        return numero

    def listar(self):
        return list(self.productos.values())

    def buscarPorCodigo(self, codigo):
        codigo = str(codigo).strip()
        producto = self.productos.get(codigo)
        if producto is None:
            raise ProductoNoEncontradoError(
                f"No existe un producto con el código '{codigo}'."
            )
        return producto

    def registrarMovimiento(self, codigo, tipo, cantidad):
        tipo = str(tipo).strip().lower()
        if tipo not in TIPOS_MOVIMIENTO:
            raise MovimientoInvalidoError(
                f"Tipo de movimiento inválido: '{tipo}'. "
                "Use 'entrada' o 'salida'."
            )
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError) as error:
            raise MovimientoInvalidoError(
                f"La cantidad '{cantidad}' no es un número entero."
            ) from error
        try:
            validarRangoNumerico(cantidad, 1, CANTIDAD_MAXIMA)
        except (TypeError, ValueError) as error:
            raise MovimientoInvalidoError(
                f"Cantidad de movimiento inválida: {error}"
            ) from error

        producto = self.buscarPorCodigo(codigo)
        if tipo == "entrada":
            existenciaFinal = producto.cantidad + cantidad
        else:
            existenciaFinal = producto.cantidad - cantidad
            if existenciaFinal < 0:
                raise ExistenciaInsuficienteError(
                    f"No hay existencia suficiente de '{producto.codigo}': "
                    f"disponible {producto.cantidad}, solicitado {cantidad}."
                )

        producto.cantidad = existenciaFinal
        movimiento = Movimiento(
            producto.codigo, tipo, cantidad, existenciaFinal
        )
        self.movimientos.append(movimiento)
        return movimiento

    def valorTotalInventario(self):
        return round(
            sum(producto.valorTotal() for producto in self.productos.values()),
            2,
        )

    def productosBajoStock(self, umbral=UMBRAL_BAJO_STOCK):
        return [
            producto
            for producto in self.productos.values()
            if producto.cantidad < umbral
        ]

    def indicadores(self):
        return {
            "totalProductos": len(self.productos),
            "valorTotal": self.valorTotalInventario(),
            "bajoStock": len(self.productosBajoStock()),
            "totalMovimientos": len(self.movimientos),
        }

    @manejarErroresArchivo
    def exportarJson(self, rutaSalida):
        datos = [producto.aDict() for producto in self.productos.values()]
        with open(rutaSalida, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
        return rutaSalida

    @manejarErroresArchivo
    def exportarCsv(self, rutaSalida):
        with open(rutaSalida, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(
                ["codigo", "producto", "cantidad", "precio", "valorTotal"]
            )
            for producto in self.productos.values():
                escritor.writerow(
                    [
                        producto.codigo,
                        producto.nombre,
                        producto.cantidad,
                        producto.precio,
                        producto.valorTotal(),
                    ]
                )
        return rutaSalida

    @manejarErroresArchivo
    def exportarMovimientosCsv(self, rutaSalida):
        with open(rutaSalida, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["codigo", "tipo", "cantidad", "existenciaFinal"])
            for movimiento in self.movimientos:
                escritor.writerow(
                    [
                        movimiento.codigo,
                        movimiento.tipo,
                        movimiento.cantidad,
                        movimiento.existenciaFinal,
                    ]
                )
        return rutaSalida
