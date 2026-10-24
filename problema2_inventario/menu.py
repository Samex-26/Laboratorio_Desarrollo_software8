from problema2_inventario.excepciones import ErrorInventario

LARGO_CODIGO = 8
LARGO_NOMBRE = 20


class MenuInventario:
    """Interfaz de consola para listar, buscar y registrar movimientos."""

    def __init__(
        self,
        gestor,
        rutaJsonSalida,
        rutaCsvInventario,
        rutaCsvMovimientos,
    ):
        self.gestor = gestor
        self.rutaJsonSalida = rutaJsonSalida
        self.rutaCsvInventario = rutaCsvInventario
        self.rutaCsvMovimientos = rutaCsvMovimientos

    @staticmethod
    def _opciones():
        return (
            "1. Listar inventario",
            "2. Buscar producto por código",
            "3. Registrar entrada",
            "4. Registrar salida",
            "5. Salir",
        )

    def _mostrarMenu(self):
        print("\n=== Menú de Inventario ===")
        for opcion in self._opciones():
            print(opcion)

    @staticmethod
    def _preguntar(mensaje):
        return input(mensaje).strip()

    def _preguntarEntero(self, mensaje):
        while True:
            try:
                return int(self._preguntar(mensaje))
            except ValueError:
                print("  Entrada inválida: ingrese un número entero.")

    @staticmethod
    def _formatoProducto(producto):
        return (
            f"{producto.codigo:<{LARGO_CODIGO}} "
            f"{producto.nombre:<{LARGO_NOMBRE}} "
            f"cant={producto.cantidad:>6} "
            f"precio={producto.precio:>10.2f} "
            f"valor={producto.valorTotal():>12.2f}"
        )

    def mostrarListado(self):
        productos = self.gestor.listar()
        print(f"\nInventario ({len(productos)} productos):")
        for producto in productos:
            print("  " + self._formatoProducto(producto))

    def buscar(self):
        codigo = self._preguntar("Código a buscar: ")
        try:
            producto = self.gestor.buscarPorCodigo(codigo)
        except ErrorInventario as error:
            print(f"  [ERROR] {error}")
            return
        print("  " + self._formatoProducto(producto))

    def registrar(self, tipo):
        codigo = self._preguntar("Código del producto: ")
        cantidad = self._preguntarEntero(f"Cantidad de {tipo}: ")
        try:
            movimiento = self.gestor.registrarMovimiento(codigo, tipo, cantidad)
        except ErrorInventario as error:
            print(f"  [ERROR] {error}")
            return
        print(
            f"  Movimiento registrado: {movimiento.tipo} de "
            f"{movimiento.cantidad} en {movimiento.codigo} "
            f"(existencia final: {movimiento.existenciaFinal})."
        )

    def mostrarIndicadores(self):
        indicadores = self.gestor.indicadores()
        print("\n=== Indicadores del inventario ===")
        print(f"Total de productos   : {indicadores['totalProductos']}")
        print(f"Valor total           : {indicadores['valorTotal']}")
        print(f"Productos con <15 un. : {indicadores['bajoStock']}")
        print(f"Movimientos registrados: {indicadores['totalMovimientos']}")

    def ejecutar(self):
        print("Bienvenido al gestor de inventario (Problema 2).")
        while True:
            self._mostrarMenu()
            try:
                opcion = self._preguntar("Seleccione una opción: ")
            except (EOFError, KeyboardInterrupt):
                print("\nSaliendo del menú...")
                break

            if opcion == "1":
                self.mostrarListado()
            elif opcion == "2":
                self.buscar()
            elif opcion == "3":
                self.registrar("entrada")
            elif opcion == "4":
                self.registrar("salida")
            elif opcion == "5":
                print("Saliendo del menú...")
                break
            else:
                print("  Opción inválida. Intente de nuevo.")

        self._exportar()
        self.mostrarIndicadores()

    def _exportar(self):
        self.gestor.exportarJson(self.rutaJsonSalida)
        self.gestor.exportarCsv(self.rutaCsvInventario)
        self.gestor.exportarMovimientosCsv(self.rutaCsvMovimientos)
        print("\nArchivos exportados:")
        print(f"  - {self.rutaJsonSalida}")
        print(f"  - {self.rutaCsvInventario}")
        print(f"  - {self.rutaCsvMovimientos}")
