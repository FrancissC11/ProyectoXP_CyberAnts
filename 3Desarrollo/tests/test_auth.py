from src.auth import EQUIPO_CYBERANTS, AuthService


def test_login_profesor_patmic_exitoso():
    auth = AuthService()
    res = auth.autenticar("patmic", "123")
    assert res["exito"] is True
    assert res["bloqueado"] is False
    assert "[+] TEAM [2]: Colonia CyberAnts" in res["mensaje"]


def test_login_6_integrantes_con_cedula_o_123():
    for miembro in EQUIPO_CYBERANTS:
        auth = AuthService()
        res_user = auth.autenticar(miembro.username, "123")
        assert res_user["exito"] is True

        auth2 = AuthService()
        res_ced = auth2.autenticar(miembro.cedula, miembro.cedula)
        assert res_ced["exito"] is True


def test_login_bloqueo_al_tercer_intento_fallido():
    auth = AuthService()
    r1 = auth.autenticar("intruso", "bad1")
    assert r1["exito"] is False
    assert r1["bloqueado"] is False
    assert r1["intentos_restantes"] == 2

    r2 = auth.autenticar("intruso", "bad2")
    assert r2["exito"] is False
    assert r2["bloqueado"] is False
    assert r2["intentos_restantes"] == 1

    r3 = auth.autenticar("intruso", "bad3")
    assert r3["exito"] is False
    assert r3["bloqueado"] is True
    assert r3["intentos_restantes"] == 0

    # Aun con credenciales válidas después del 3er fallo sigue bloqueado
    r4 = auth.autenticar("patmic", "123")
    assert r4["exito"] is False
    assert r4["bloqueado"] is True


def test_login_credenciales_vacias_no_crashea():
    auth = AuthService()
    res = auth.autenticar("", None)
    assert res["exito"] is False
    assert auth.intentos_fallidos == 1
