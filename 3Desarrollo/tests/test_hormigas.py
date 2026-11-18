from src.app import create_app
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

    # HSoldado muere si recibe un alimento distinto a Carnívoro (ej. Néctar)
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


def test_rutas_flask_principales(tmp_path):
    app = create_app(db_path=tmp_path / "test.db")
    client = app.test_client()

    # Login como patmic
    resp = client.post("/login", data={"username": "patmic", "password": "123"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Colonia CyberAnts" in resp.data
    assert b"Verificar Archivo Alterno" not in resp.data

    # Vista dron y hormiguero (solo HLarva y HSoldado)
    assert client.get("/dron").status_code == 200
    resp_h = client.get("/hormiguero")
    assert resp_h.status_code == 200
    assert b"HSoldado" in resp_h.data
    assert b"HZangano" not in resp_h.data
