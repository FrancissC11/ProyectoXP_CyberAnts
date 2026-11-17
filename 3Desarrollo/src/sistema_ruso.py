from dataclasses import dataclass, field
from pathlib import Path
from src.contracts import Utility


@dataclass
class CoordenadaUK:
    """Representa una fila desencriptada del archivo ucraniano Grupo##.csv."""

    geoposicion: str
    lunes: str
    martes: str
    miercoles: str
    jueves: str
    viernes: str
    tipoArsenal: str
    loading_final: str = "100%"
    pasos_loading: list[str] = field(default_factory=Utility.generar_pasos_loading)

    def to_console_line(self) -> str:
        return (
            f"{self.loading_final:<7} "
            f"{self.geoposicion:<8}| "
            f"{self.lunes:<6}| "
            f"{self.martes:<6}| "
            f"{self.miercoles:<9}| "
            f"{self.jueves:<6}| "
            f"{self.viernes:<7}| "
            f"{self.tipoArsenal}"
        )


class SistemaRuso:
    """Sistema Ruso encargado de leer y procesar las coordenadas de Grupo##.csv."""

    def __init__(self):
        self.ultimo_error: str | None = None
        self.advertencias: list[str] = []

    def readCoord(self, fileName: str | Path) -> list[CoordenadaUK]:
        """
        Lee el archivo CSV separado por ';' y devuelve la lista de CoordenadaUK.
        Si el archivo no existe o hay filas malformadas, registra un error controlado
        sin provocar ningún crash.
        """
        self.ultimo_error = None
        self.advertencias = []
        ruta = Path(fileName)

        if not ruta.exists() or not ruta.is_file():
            self.ultimo_error = f"Archivo de coordenadas no encontrado: {ruta}"
            return []

        coordenadas: list[CoordenadaUK] = []
        try:
            contenido = ruta.read_text(encoding="utf-8")
        except Exception as exc:
            self.ultimo_error = f"Error al leer el archivo CSV: {exc}"
            return []

        lineas = [ln.strip() for ln in contenido.splitlines() if ln.strip()]
        if not lineas:
            self.ultimo_error = "El archivo CSV está vacío."
            return []

        for num_linea, linea in enumerate(lineas, start=1):
            # Ignorar cabecera si empieza con Geoposición / Geoposicion
            if num_linea == 1 and linea.lower().startswith("geoposic"):
                continue

            partes = [p.strip() for p in linea.split(";")]
            if len(partes) != 7:
                self.advertencias.append(
                    f"Línea {num_linea} malformada (se esperaban 7 columnas separadas por ';'): '{linea}'"
                )
                continue

            geopos, lun, mar, mie, jue, vie, arsenal = partes
            if not geopos or not arsenal:
                self.advertencias.append(
                    f"Línea {num_linea} incompleta (Geoposición o Tipo Arsenal vacío): '{linea}'"
                )
                continue

            coordenadas.append(
                CoordenadaUK(
                    geoposicion=geopos,
                    lunes=lun,
                    martes=mar,
                    miercoles=mie,
                    jueves=jue,
                    viernes=vie,
                    tipoArsenal=arsenal,
                )
            )

        if not coordenadas and not self.ultimo_error:
            self.ultimo_error = "No se encontraron coordenadas válidas en el CSV."

        return coordenadas
