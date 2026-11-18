from pathlib import Path
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from src.auth import EQUIPO_CYBERANTS, AuthService
from src.console import DEFAULT_CSV
from src.db import CyberAntsDB
from src.dron import AntCiberDron, ExpertoIdioma
from src.sistema_ruso import SistemaRuso

BASE_DIR = Path(__file__).resolve().parent


def create_app(db_path: str | Path | None = None, csv_path: str | Path | None = None) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.secret_key = "kgd-antdron-tactical-secret-key"

    app_db = CyberAntsDB(db_path) if db_path else CyberAntsDB()
    app_csv = Path(csv_path) if csv_path else DEFAULT_CSV
    auth_service = AuthService()
    dron_instance = AntCiberDron()

    app.config["CYBERANTS_DB"] = app_db
    app.config["CYBERANTS_CSV"] = app_csv
    app.config["AUTH_SERVICE"] = auth_service
    app.config["DRON_INSTANCE"] = dron_instance

    @app.context_processor
    def inject_globals():
        return {
            "usuario_actual": session.get("usuario_autenticado"),
            "grupo_numero": AuthService.GRUPO_NUMERO,
            "grupo_nombre": AuthService.GRUPO_NOMBRE,
        }

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            usuario = request.form.get("username", "")
            password = request.form.get("password", "")
            res = auth_service.autenticar(usuario, password)
            if res["exito"]:
                session["usuario_autenticado"] = res["usuario"]
                flash(f"Acceso concedido: {res['usuario']}", "ok")
                return redirect(url_for("coordenadas"))
            flash(res["mensaje"], "error")

        return render_template(
            "login.html",
            bloqueado=auth_service.bloqueado,
            intentos_fallidos=auth_service.intentos_fallidos,
            intentos_restantes=auth_service.intentos_restantes,
            equipo=EQUIPO_CYBERANTS,
        )

    @app.route("/login/reset", methods=["POST"])
    def login_reset():
        auth_service.reiniciar_intentos()
        session.pop("usuario_autenticado", None)
        flash("Terminal de seguridad KGD reiniciada (3 intentos disponibles).", "info")
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        session.pop("usuario_autenticado", None)
        return redirect(url_for("login"))

    @app.route("/")
    def coordenadas():
        if not session.get("usuario_autenticado"):
            return redirect(url_for("login"))

        sistema = SistemaRuso()
        lista_coord = sistema.readCoord(app_csv)
        evaluaciones = dron_instance.evaluar_coordenadas(lista_coord)

        return render_template(
            "coordenadas.html",
            equipo=EQUIPO_CYBERANTS,
            coordenadas=lista_coord,
            evaluaciones=evaluaciones,
            error_csv=sistema.ultimo_error,
            advertencias_csv=sistema.advertencias,
        )

    @app.route("/dron", methods=["GET", "POST"])
    def dron():
        if not session.get("usuario_autenticado"):
            return redirect(url_for("login"))

        sistema = SistemaRuso()
        lista_coord = sistema.readCoord(app_csv)
        evaluaciones = dron_instance.evaluar_coordenadas(lista_coord)
        resultado_prueba = None

        if request.method == "POST":
            accion_form = request.form.get("form_action", "")

            if accion_form == "probar_palabra":
                palabra = request.form.get("palabra", "")
                explota = dron_instance.buscar(palabra)
                traza = dron_instance.automata.trazar(palabra)
                resultado_prueba = {
                    "palabra": palabra if palabra else "(cadena vacía ε)",
                    "explota": explota,
                    "accion_str": "true" if explota else "false",
                    "recorrido": " -> ".join(traza["recorrido"]),
                }

            elif accion_form == "subsistema":
                operacion = request.form.get("operacion", "")
                if operacion == "volar":
                    if dron_instance.volar():
                        flash("TurboReactor activado: AntCiberDron en vuelo táctico (-20% energía).", "ok")
                    else:
                        flash("Energía insuficiente en FuentePoder para activar el TurboReactor.", "error")
                elif operacion == "metralleta":
                    if dron_instance.disparar_metralleta():
                        flash("Pata delantera derecha: ráfaga de metralleta ejecutada (-15 munición).", "ok")
                    else:
                        flash("Metralleta sin munición disponible.", "error")
                elif operacion == "laser":
                    potencia = dron_instance.disparar_laser()
                    if potencia > 0:
                        flash(f"Pata delantera izquierda: disparo láser a {potencia} kW (-15% energía).", "ok")
                    else:
                        flash("Energía insuficiente para disparar el láser.", "error")
                elif operacion == "recargar":
                    dron_instance.asistir_fuente_poder("recargar")
                    flash("IIA: FuentePoder recargada al 100%.", "ok")
                elif operacion == "reemplazar":
                    dron_instance.asistir_fuente_poder("reemplazar")
                    flash("IIA: FuentePoder reemplazada por núcleo nuevo al 100%.", "ok")

            elif accion_form == "entrenar_idioma":
                nombre_exp = request.form.get("experto_nombre", "")
                idioma_exp = request.form.get("experto_idioma", "")
                es_experto = request.form.get("es_experto", "si") == "si"
                lexico_raw = request.form.get("lexico", "")
                gramatica = request.form.get("gramatica", "")
                fonetica = request.form.get("fonetica", "")

                try:
                    if not es_experto:
                        # Simulación de intento por personal no experto (debe ser rechazado por IIA)
                        dron_instance.entrenar_idioma(
                            "OperadorNoExperto",  # type: ignore[arg-type]
                            [w.strip() for w in lexico_raw.split(",")],
                            gramatica,
                            fonetica,
                        )
                    else:
                        experto = ExpertoIdioma(nombre=nombre_exp, idioma=idioma_exp)
                        lexico_lista = [w.strip() for w in lexico_raw.split(",") if w.strip()]
                        dron_instance.entrenar_idioma(experto, lexico_lista, gramatica, fonetica)
                        flash(
                            f"Idioma '{experto.idioma}' entrenado exitosamente por {experto.nombre}.",
                            "ok",
                        )
                except (PermissionError, ValueError) as exc:
                    flash(f"Entrenamiento rechazado: {exc}", "error")

        return render_template(
            "dron.html",
            dron=dron_instance,
            evaluaciones=evaluaciones,
            destruir=[e for e in evaluaciones if e["accion"]],
            resultado_prueba=resultado_prueba,
        )

    @app.route("/hormiguero", methods=["GET"])
    def hormiguero():
        if not session.get("usuario_autenticado"):
            return redirect(url_for("login"))

        hormigas = app_db.listar_hormigas()
        historial = app_db.listar_historial()
        return render_template(
            "hormiguero.html",
            hormigas=hormigas,
            historial=historial,
        )

    @app.route("/hormiguero/crear", methods=["POST"])
    def hormiguero_crear():
        if not session.get("usuario_autenticado"):
            return redirect(url_for("login"))

        sexo = request.form.get("sexo", "Asexual")
        nueva = app_db.crear_hormiga(sexo=sexo)
        flash(f"Creada {nueva.toString()} (nace como HLarva).", "ok")
        return redirect(url_for("hormiguero"))

    @app.route("/hormiguero/alimentar", methods=["POST"])
    def hormiguero_alimentar():
        if not session.get("usuario_autenticado"):
            return redirect(url_for("login"))

        try:
            id_hormiga = int(request.form.get("id_hormiga", "0"))
            alimento = request.form.get("alimento", "Néctar")
            res = app_db.alimentar_hormiga(id_hormiga, alimento)
            if res["sobrevive"]:
                if res["tipo_anterior"] != res["tipo_nuevo"]:
                    flash(
                        f"Hormiga #{id_hormiga} comió {res['alimento']} y evolucionó de "
                        f"{res['tipo_anterior']} a {res['tipo_nuevo']} (Estado: {res['hormiga'].estado}).",
                        "ok",
                    )
                else:
                    flash(
                        f"Hormiga #{id_hormiga} comió {res['alimento']} y sigue {res['hormiga'].estado} "
                        f"como {res['tipo_nuevo']}.",
                        "ok",
                    )
            else:
                flash(
                    f"Hormiga #{id_hormiga} ({res['tipo_anterior']}) comió {res['alimento']} incompatible "
                    f"y pasó a estado {res['hormiga'].estado}.",
                    "error",
                )
        except Exception as exc:
            flash(f"Operación controlada: {exc}", "error")

        return redirect(url_for("hormiguero"))

    @app.route("/hormiguero/reiniciar", methods=["POST"])
    def hormiguero_reiniciar():
        if not session.get("usuario_autenticado"):
            return redirect(url_for("login"))
        app_db.reiniciar_hormiguero()
        flash("Hormiguero Virtual reiniciado con 2 larvas base (HLarva).", "info")
        return redirect(url_for("hormiguero"))

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "system": "ANTDRON-KGD", "group": AuthService.GRUPO_NOMBRE})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
