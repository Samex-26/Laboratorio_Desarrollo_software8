import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))


def ejecutarProblema1():
    from problema1_estudiantes.excepciones import ErrorEstudiante
    try:
        from problema1_estudiantes.main_p1 import main as mainP1
        mainP1()
    except ErrorEstudiante as error:
        print(f"[ERROR] {error}")
    except (FileNotFoundError, PermissionError) as error:
        print(f"[ERROR] {error}")
    except (EOFError, KeyboardInterrupt):
        print("\n[INFO] Ejecucion del Problema 1 interrumpida.")


def ejecutarProblema2():
    from problema2_inventario.excepciones import ErrorInventario
    try:
        from problema2_inventario.main_p2 import main as mainP2
        mainP2()
    except ErrorInventario as error:
        print(f"[ERROR] {error}")
    except (FileNotFoundError, PermissionError) as error:
        print(f"[ERROR] {error}")
    except (EOFError, KeyboardInterrupt):
        print("\n[INFO] Ejecucion del Problema 2 interrumpida.")


def ejecutarProblema3():
    from problema3_sensores.procesador import ErrorSensores
    try:
        from problema3_sensores.main_p3 import main as mainP3
        mainP3()
    except ErrorSensores as error:
        print(f"[ERROR] {error}")
    except (FileNotFoundError, PermissionError) as error:
        print(f"[ERROR] {error}")
    except (EOFError, KeyboardInterrupt):
        print("\n[INFO] Ejecucion del Problema 3 interrumpida.")


def _mostrarMenu():
    print("\n============================================")
    print("  Lab2_software8 - Menu de integracion")
    print("============================================")
    print("  1) Ejecutar Problema 1 (Estudiantes)")
    print("  2) Ejecutar Problema 2 (Inventario)")
    print("  3) Ejecutar Problema 3 (Sensores IoT)")
    print("  4) Salir")


def main():
    while True:
        _mostrarMenu()
        try:
            opcion = input("Seleccione una opcion: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            return 0

        try:
            if opcion == "1":
                ejecutarProblema1()
            elif opcion == "2":
                ejecutarProblema2()
            elif opcion == "3":
                ejecutarProblema3()
            elif opcion == "4":
                print("Saliendo...")
                return 0
            else:
                print("Opcion invalida. Intente de nuevo.")
        except Exception as error:
            print(f"[ERROR] Fallo inesperado: {error}")


if __name__ == "__main__":
    sys.exit(main())
