import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from problema1_estudiantes.excepciones import ErrorEstudiante
from problema1_estudiantes.gestor import GestorEstudiantes


def main():
    rutaCsv = RAIZ_PROYECTO / "data" / "estudiantes.csv"
    rutaJson = RAIZ_PROYECTO / "output" / "estudiantes.json"
    rutaResumen = RAIZ_PROYECTO / "output" / "resumen.txt"

    gestor = GestorEstudiantes(rutaCsv)
    try:
        indicadores = gestor.procesar(rutaJson, rutaResumen)
    except ErrorEstudiante as error:
        print(f"[ERROR] {error}")
        return 1
    except (FileNotFoundError, PermissionError) as error:
        print(f"[ERROR] {error}")
        return 1

    print("Problema 1 - Estudiantes (CSV -> JSON)")
    print(f"Registros cargados : {indicadores['totalEstudiantes']}")
    print(f"Promedio general   : {indicadores['promedioGeneral']}")
    print(f"Nota mayor         : {indicadores['notaMayor']}")
    print(f"Nota menor         : {indicadores['notaMenor']}")
    print(f"Aprobados          : {indicadores['aprobados']}")
    print(f"Reprobados         : {indicadores['reprobados']}")
    print(f"JSON exportado en  : {rutaJson}")
    print(f"Resumen exportado en: {rutaResumen}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
