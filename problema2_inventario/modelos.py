class Producto:

    def __init__(self, codigo, nombre, cantidad, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def valorTotal(self):
        return round(self.cantidad * self.precio, 2)

    def aDict(self):
        return {
            "codigo": self.codigo,
            "producto": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "valor_total": self.valorTotal(),
        }

    def __repr__(self):
        return (
            f"Producto(codigo={self.codigo!r}, nombre={self.nombre!r}, "
            f"cantidad={self.cantidad!r}, precio={self.precio!r})"
        )


class Movimiento:

    def __init__(self, codigo, tipo, cantidad, existenciaFinal):
        self.codigo = codigo
        self.tipo = tipo
        self.cantidad = cantidad
        self.existenciaFinal = existenciaFinal

    def aDict(self):
        return {
            "codigo": self.codigo,
            "tipo": self.tipo,
            "cantidad": self.cantidad,
            "existencia_final": self.existenciaFinal,
        }

    def __repr__(self):
        return (
            f"Movimiento(codigo={self.codigo!r}, tipo={self.tipo!r}, "
            f"cantidad={self.cantidad!r}, existencia_final={self.existenciaFinal!r})"
        )
