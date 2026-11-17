import pytest
from src.dron import AntCiberDron, ExpertoIdioma


@pytest.mark.parametrize(
    "palabra_valida",
    ["a", "aa", "aaaa", "ab", "abb", "abbb", "at", "att", "abt", "abtt", "abbtt", "abcdt", "abcdttt", "abcdttttt"],
)
def test_automata_acepta_lenguaje_del_grupo(palabra_valida):
    dron = AntCiberDron()
    assert dron.buscar(palabra_valida) is True


@pytest.mark.parametrize(
    "palabra_invalida",
    ["", "   ", "b", "ba", "aba", "aab", "t", "bt", "abc", "abcd", "abcdd", "abtc", "xyz", None],
)
def test_automata_rechaza_fuera_del_lenguaje_y_vacio(palabra_invalida):
    dron = AntCiberDron()
    assert dron.buscar(palabra_invalida) is False  # type: ignore[arg-type]


def test_subsistemas_energia_vuelo_y_armas():
    dron = AntCiberDron()
    assert dron.fuente_poder.energia == 100
    assert dron.volar() is True
    assert dron.turbo_reactor.en_vuelo is True
    assert dron.fuente_poder.energia == 80

    potencia = dron.disparar_laser()
    assert potencia == 120  # 80 * 1.5 kW
    assert dron.fuente_poder.energia == 65
    assert dron.disparar_metralleta() is True
    assert dron.metralleta.municion == 135

    dron.asistir_fuente_poder("reemplazar")
    assert dron.fuente_poder.energia == 100
    assert dron.fuente_poder.reemplazos == 1


def test_entrenamiento_idiomas_solo_expertos():
    dron = AntCiberDron()
    exp_en = ExpertoIdioma("Dr. Smith", "ingles")
    reg = dron.entrenar_idioma(exp_en, ["strike", "hold"], "SVO", "/straɪk/")
    assert reg["experto"] == "Dr. Smith"

    with pytest.raises(ValueError):
        ExpertoIdioma("Pierre", "frances")

    with pytest.raises(PermissionError):
        dron.entrenar_idioma("NoSoyExperto", ["hola"], "SVO", "/ola/")  # type: ignore[arg-type]
