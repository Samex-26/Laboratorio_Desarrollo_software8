import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from problema3_sensores.procesador import ErrorSensores, ProcesadorSensores


def _imprimirTabla(titulo, dataframe):
    print(f"\n{titulo}:")
    columnas = list(dataframe.columns)
    filas = dataframe.to_dicts()

    def esNumerico(valor):
        return isinstance(valor, (int, float)) and not isinstance(valor, bool)

    textos = []
    for fila in filas:
        textosFila = []
        for columna in columnas:
            valor = fila[columna]
            if isinstance(valor, float):
                textosFila.append(f"{valor:.2f}")
            else:
                textosFila.append(str(valor))
        textos.append(textosFila)

    anchos = []
    for indice, columna in enumerate(columnas):
        ancho = len(columna)
        for textosFila in textos:
            ancho = max(ancho, len(textosFila[indice]))
        anchos.append(ancho)

    columnasNumericas = [
        all(esNumerico(fila[columna]) for fila in filas) for columna in columnas
    ]

    def unir(celdas):
        partes = []
        for indice, celda in enumerate(celdas):
            if columnasNumericas[indice]:
                partes.append(f"{celda:>{anchos[indice]}}")
            else:
                partes.append(f"{celda:<{anchos[indice]}}")
        return "  " + " | ".join(partes)

    print(unir(columnas))
    for textosFila in textos:
        print(unir(textosFila))


def main():
    rutaCsv = RAIZ_PROYECTO / "data" / "sensores.csv"
    rutaAlertas = RAIZ_PROYECTO / "output" / "alertas.json"
    rutaResumen = RAIZ_PROYECTO / "output" / "resumen_sensores.csv"
    rutaProcesados = RAIZ_PROYECTO / "output" / "sensores_procesados.json"

    procesador = ProcesadorSensores(rutaCsv)
    try:
        procesador.procesar()
        procesador.exportar(rutaAlertas, rutaResumen, rutaProcesados)
    except ErrorSensores as error:
        print(f"[ERROR] {error}")
        return 1
    except (FileNotFoundError, PermissionError) as error:
        print(f"[ERROR] {error}")
        return 1

    reporte = procesador.resumenReporte()
    print("Problema 3 - Sensores IoT (Polars %s)" % __import__("polars").__version__)
    print(f"Archivo de entrada : {rutaCsv}")
    print("\n=== Reporte de validación ===")
    print(f"Total de registros leídos     : {reporte['totalLeidos']}")
    print(f"Registros válidos             : {reporte['validos']}")
    print(f"Descartados incompletos       : {reporte['descartadosIncompletos']}")
    print(f"Descartados fuera de rango    : {reporte['descartadosFueraRango']}")
    print(f"Total de alertas              : {reporte['totalAlertas']}")

    _imprimirTabla(
        "Muestra del DataFrame procesado (primeros 6 registros)",
        procesador.dfProcesado.head(6).select(
            ["sensor", "ubicacion", "temperatura", "humedad", "estado", "motivo"]
        ),
    )
    _imprimirTabla(
        "Resumen por sensor",
        procesador.resumenPorSensor,
    )
    _imprimirTabla(
        "Humedad promedio por ubicación",
        procesador.resumenPorUbicacion,
    )
    _imprimirTabla(
        "Alertas detectadas",
        procesador.alertas,
    )

    print("\nArchivos exportados:")
    print(f"  - {rutaAlertas}")
    print(f"  - {rutaResumen}")
    print(f"  - {rutaProcesados}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
