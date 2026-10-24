import csv
import json

from common.io_utils import manejarErroresArchivo
from common.validadores import validarNoVacio, validarRangoNumerico

from problema1_estudiantes.excepciones import (
    ArchivoEstudiantesError,
    CedulaDuplicadaError,
    NotaFueraDeRangoError,
    RegistroInvalidoError,
)
from problema1_estudiantes.modelos import Estudiante

COLUMNAS_REQUERIDAS = ("cedula", "nombre", "parcial1", "parcial2", "proyecto")
CAMPOS_NUMERICOS = ("parcial1", "parcial2", "proyecto")
MINIMO_REGISTROS = 20
NOTA_MINIMA = 0
NOTA_MAXIMA = 100


class GestorEstudiantes:

    def __init__(self, rutaCsv):
        self.rutaCsv = rutaCsv
        self.estudiantes = []
        self._cedulas = set()

    @manejarErroresArchivo
    def cargar(self):
        with open(self.rutaCsv, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            self._validarCabecera(lector.fieldnames)
            for numeroFila, fila in enumerate(lector, start=2):
                self._procesarFila(fila, numeroFila)

        if len(self.estudiantes) < MINIMO_REGISTROS:
            raise ArchivoEstudiantesError(
                f"El archivo '{self.rutaCsv}' debe contener al menos "
                f"{MINIMO_REGISTROS} registros válidos; se encontraron "
                f"{len(self.estudiantes)}."
            )
        return self.estudiantes

    @staticmethod
    def _validarCabecera(fieldnames):
        if not fieldnames:
            raise ArchivoEstudiantesError(
                "El archivo CSV está vacío o no tiene una fila de encabezado."
            )
        faltantes = [
            columna for columna in COLUMNAS_REQUERIDAS if columna not in fieldnames
        ]
        if faltantes:
            raise ArchivoEstudiantesError(
                "Al archivo CSV le faltan las columnas requeridas: "
                + ", ".join(faltantes)
            )

    def _procesarFila(self, fila, numeroFila):
        for campo in COLUMNAS_REQUERIDAS:
            try:
                validarNoVacio(fila.get(campo), campo)
            except ValueError as error:
                raise RegistroInvalidoError(
                    f"Fila {numeroFila}: {error}"
                ) from error

        notas = {}
        for campo in CAMPOS_NUMERICOS:
            try:
                nota = float(fila[campo])
            except (TypeError, ValueError) as error:
                raise RegistroInvalidoError(
                    f"Fila {numeroFila}: la nota '{campo}' "
                    f"('{fila[campo]}') no es numérica."
                ) from error
            try:
                validarRangoNumerico(nota, NOTA_MINIMA, NOTA_MAXIMA)
            except (TypeError, ValueError) as error:
                raise NotaFueraDeRangoError(
                    f"Fila {numeroFila}: la nota '{campo}' ({nota}) es "
                    f"inválida. {error}"
                ) from error
            notas[campo] = nota

        cedula = fila["cedula"].strip()
        if cedula in self._cedulas:
            raise CedulaDuplicadaError(
                f"Fila {numeroFila}: la cédula '{cedula}' está duplicada."
            )
        self._cedulas.add(cedula)

        estudiante = Estudiante(
            cedula,
            fila["nombre"].strip(),
            notas["parcial1"],
            notas["parcial2"],
            notas["proyecto"],
        )
        estudiante.calcularNotaFinal()
        estudiante.clasificar()
        self.estudiantes.append(estudiante)

    def calcularIndicadores(self):
        if not self.estudiantes:
            raise ArchivoEstudiantesError(
                "No hay estudiantes cargados para calcular indicadores."
            )
        notas = [estudiante.notaFinal for estudiante in self.estudiantes]
        aprobados = sum(
            1 for estudiante in self.estudiantes if estudiante.condicion == "APROBADO"
        )
        reprobados = len(self.estudiantes) - aprobados
        return {
            "totalEstudiantes": len(self.estudiantes),
            "promedioGeneral": round(sum(notas) / len(notas), 2),
            "notaMayor": max(notas),
            "notaMenor": min(notas),
            "aprobados": aprobados,
            "reprobados": reprobados,
        }

    @manejarErroresArchivo
    def exportarJson(self, rutaSalida):
        datos = [estudiante.aDict() for estudiante in self.estudiantes]
        with open(rutaSalida, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
        return rutaSalida

    @manejarErroresArchivo
    def exportarResumen(self, rutaSalida, indicadores):
        lineas = [
            "Resumen del grupo - Problema 1 (Estudiantes)",
            "=" * 45,
            f"Total de estudiantes : {indicadores['totalEstudiantes']}",
            f"Promedio general     : {indicadores['promedioGeneral']}",
            f"Nota mayor           : {indicadores['notaMayor']}",
            f"Nota menor           : {indicadores['notaMenor']}",
            f"Aprobados            : {indicadores['aprobados']}",
            f"Reprobados           : {indicadores['reprobados']}",
            "",
        ]
        with open(rutaSalida, "w", encoding="utf-8") as archivo:
            archivo.write("\n".join(lineas))
        return rutaSalida

    def procesar(self, rutaJson, rutaResumen):
        self.cargar()
        indicadores = self.calcularIndicadores()
        self.exportarJson(rutaJson)
        self.exportarResumen(rutaResumen, indicadores)
        return indicadores
