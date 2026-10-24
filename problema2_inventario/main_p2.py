import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from problema2_inventario.excepciones import ErrorInventario
from problema2_inventario.gestor import GestorInventario
from problema2_inventario.menu import MenuInventario


def main():
    rutaEntrada = RAIZ_PROYECTO / "data" / "inventario.json"
    rutaJsonSalida = RAIZ_PROYECTO / "output" / "inventario_actualizado.json"
    rutaCsvInventario = RAIZ_PROYECTO / "output" / "inventario.csv"
    rutaCsvMovimientos = RAIZ_PROYECTO / "output" / "movimientos.csv"

    gestor = GestorInventario()
    try:
        gestor.cargarJson(rutaEntrada)
    except ErrorInventario as error:
        print(f"[ERROR] {error}")
        return 1
    except (FileNotFoundError, PermissionError) as error:
        print(f"[ERROR] {error}")
        return 1

    print(f"Inventario cargado desde: {rutaEntrada}")

    menu = MenuInventario(
        gestor,
        rutaJsonSalida,
        rutaCsvInventario,
        rutaCsvMovimientos,
    )
    menu.ejecutar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
