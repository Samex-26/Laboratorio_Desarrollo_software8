from pathlib import Path

import polars as pl

from common.io_utils import manejarErroresArchivo

TEMP_ALERTA = 32.0
HUM_ALERTA = 80.0
TEMP_MIN = 0.0
TEMP_MAX = 100.0
HUM_MIN = 0.0
HUM_MAX = 100.0
MIN_MEDICIONES = 20

COLUMNAS_REQUERIDAS = ("sensor", "ubicacion", "temperatura", "humedad")
COLUMNAS_NUMERICAS = ("temperatura", "humedad")
COLUMNA_UBICACION = "ubicacion"
VALORES_NULOS = ["", "NA", "N/A", "null", "None"]


class ErrorSensores(Exception):
    """Excepción propia del Procesador de Sensores."""


class ProcesadorSensores:
    def __init__(self, rutaCsv):
        self.rutaCsv = Path(rutaCsv)
        self.dfProcesado = None
        self.reporte = {}

    def _exprAlertaTemperatura(self):
        return pl.col("temperatura") > TEMP_ALERTA

    def _exprAlertaHumedad(self):
        return pl.col("humedad") > HUM_ALERTA

    @manejarErroresArchivo
    def cargar(self):
        df = pl.read_csv(
            self.rutaCsv,
            infer_schema_length=1000,
            null_values=VALORES_NULOS,
            schema_overrides={
                "temperatura": pl.Float64,
                "humedad": pl.Float64,
            },
        )
        faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
        if faltantes:
            raise ErrorSensores(
                "Al archivo de sensores le faltan las columnas requeridas: "
                + ", ".join(faltantes)
            )
        if df.height < MIN_MEDICIONES:
            raise ErrorSensores(
                f"El archivo debe contener al menos {MIN_MEDICIONES} mediciones; "
                f"se encontraron {df.height}."
            )
        self.dfProcesado = df
        return df

    def limpiarYValidar(self):
        df = self.dfProcesado
        totalLeidos = df.height

        dfCompleto = df.drop_nulls(subset=list(COLUMNAS_REQUERIDAS))
        descartadosIncompletos = totalLeidos - dfCompleto.height

        dfValido = dfCompleto.filter(
            pl.col("temperatura").is_between(TEMP_MIN, TEMP_MAX)
            & pl.col("humedad").is_between(HUM_MIN, HUM_MAX)
        )
        descartadosFueraRango = dfCompleto.height - dfValido.height

        self.dfProcesado = dfValido
        self.reporte = {
            "totalLeidos": totalLeidos,
            "validos": dfValido.height,
            "descartadosIncompletos": descartadosIncompletos,
            "descartadosFueraRango": descartadosFueraRango,
        }
        if dfValido.height < MIN_MEDICIONES:
            raise ErrorSensores(
                f"Tras la limpieza quedan {dfValido.height} mediciones válidas; "
                f"se requieren al menos {MIN_MEDICIONES}."
            )
        return self.dfProcesado

    def clasificar(self):
        alertaTemp = self._exprAlertaTemperatura()
        alertaHumedad = self._exprAlertaHumedad()

        estado = (
            pl.when(alertaTemp | alertaHumedad)
            .then(pl.lit("ALERTA"))
            .otherwise(pl.lit("NORMAL"))
        )
        motivo = (
            pl.when(alertaTemp & alertaHumedad)
            .then(pl.lit("ambas"))
            .when(alertaTemp)
            .then(pl.lit("temperatura"))
            .when(alertaHumedad)
            .then(pl.lit("humedad"))
            .otherwise(pl.lit(None, dtype=pl.String))
        )
        self.dfProcesado = self.dfProcesado.with_columns(
            estado.alias("estado"),
            motivo.alias("motivo"),
        )
        return self.dfProcesado

    def calcularPorSensor(self):
        return (
            self.dfProcesado.group_by("sensor")
            .agg(
                pl.col("ubicacion").first().alias("ubicacion"),
                pl.col("temperatura").count().alias("mediciones"),
                pl.col("temperatura").mean().alias("temperaturaPromedio"),
                pl.col("temperatura").max().alias("temperaturaMaxima"),
                pl.col("temperatura").min().alias("temperaturaMinima"),
                pl.col("humedad").mean().alias("humedadPromedio"),
            )
            .sort("sensor")
        )

    def calcularHumedadPorUbicacion(self):
        return (
            self.dfProcesado.group_by(COLUMNA_UBICACION)
            .agg(
                pl.col("humedad").mean().alias("humedadPromedio"),
                pl.col("humedad").count().alias("mediciones"),
            )
            .sort(COLUMNA_UBICACION)
        )

    def obtenerAlertas(self):
        columnas = [
            "sensor",
            "ubicacion",
            "fecha",
            "hora",
            "temperatura",
            "humedad",
            "motivo",
        ]
        disponibles = [c for c in columnas if c in self.dfProcesado.columns]
        return (
            self.dfProcesado.filter(pl.col("estado") == "ALERTA")
            .select(disponibles)
            .sort("sensor")
        )

    def procesar(self):
        self.cargar()
        self.limpiarYValidar()
        self.clasificar()
        self.resumenPorSensor = self.calcularPorSensor()
        self.resumenPorUbicacion = self.calcularHumedadPorUbicacion()
        self.alertas = self.obtenerAlertas()
        self.reporte["totalAlertas"] = self.alertas.height
        return self

    @manejarErroresArchivo
    def exportar(self, rutaAlertas, rutaResumen, rutaProcesados):
        self.alertas.write_json(rutaAlertas)
        self.resumenPorSensor.write_csv(rutaResumen)
        self.dfProcesado.write_json(rutaProcesados)
        return (rutaAlertas, rutaResumen, rutaProcesados)

    def resumenReporte(self):
        return dict(self.reporte)
