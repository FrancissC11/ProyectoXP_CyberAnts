from pathlib import Path
from src.contracts import Utility
from src.sistema_ruso import SistemaRuso


def test_lectura_csv_grupo02_exitosa():
    csv_path = Path(__file__).resolve().parent.parent / "data" / "Grupo02.csv"
    sistema = SistemaRuso()
    coords = sistema.readCoord(csv_path)

    assert sistema.ultimo_error is None
    assert len(coords) == 60
    assert coords[0].geoposicion == "Coord-00"
    assert coords[0].tipoArsenal == "aa"
    assert coords[-1].geoposicion == "Coord-02"
    assert coords[0].pasos_loading[-1] == "100%"


def test_loading_secuencia_simbolos():
    pasos = Utility.generar_pasos_loading()
    assert pasos[0].startswith("\\")
    assert pasos[1].startswith("|")
    assert pasos[2].startswith("/")
    assert pasos[3].startswith("-")
    assert pasos[-1] == "100%"


def test_csv_inexistente_no_crashea(tmp_path):
    sistema = SistemaRuso()
    coords = sistema.readCoord(tmp_path / "no_existe.csv")
    assert coords == []
    assert sistema.ultimo_error is not None


def test_csv_filas_malformadas_se_ignoran_sin_crash(tmp_path):
    archivo = tmp_path / "malformado.csv"
    archivo.write_text(
        "Geoposición ; Lunes ; Martes ; Miércoles ; Jueves ; Viernes ; Tipo Arsenal\n"
        "fila_rota_sin_puntos_y_coma\n"
        "Coord-01; 01-02 ; ; ; ; ; aaaa\n",
        encoding="utf-8",
    )
    sistema = SistemaRuso()
    coords = sistema.readCoord(archivo)
    assert len(coords) == 1
    assert coords[0].geoposicion == "Coord-01"
    assert len(sistema.advertencias) == 1
    