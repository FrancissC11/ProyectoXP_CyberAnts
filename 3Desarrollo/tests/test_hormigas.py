from src.db import CyberAntsDB
from src.hormigas import (
    ACarnivoro,
    ANectar,
    HLarva,
    HormigueroVirtual,
    HSoldado,
)


def test_hlarva_vive_con_nectar():
    h = HLarva(id=1)
    assert h.comer(ANectar()) is True
    assert isinstance(h, HLarva)
    assert h.estado == "VIVA"


def test_hlarva_evoluciona_a_hsoldado_con_carnivoro_y_muere_con_otro():
    h_soldado = HLarva(id=10)
    assert h_soldado.comer(ACarnivoro()) is True
    assert isinstance(h_soldado, HSoldado)
    assert h_soldado.sexo == "Macho"
    assert h_soldado.comer(ACarnivoro()) is True
    assert h_soldado.estado == "VIVA"

    assert h_soldado.comer(ANectar()) is False
    assert h_soldado.estado == "MUERTA"


def test_hormiguero_virtual_y_sqlite(tmp_path):
    colonia = HormigueroVirtual()
    larva = colonia.crear_hormiga("Asexual")
    assert colonia.alimentar_hormiga(larva.id, ACarnivoro()) is True
    assert larva.tipo == "HSoldado"

    db = CyberAntsDB(tmp_path / "test_c4.db")
    creada = db.crear_hormiga("Asexual")
    res = db.alimentar_hormiga(creada.id, "Carnívoro")
    assert res["tipo_nuevo"] == "HSoldado"
    assert res["sobrevive"] is True
