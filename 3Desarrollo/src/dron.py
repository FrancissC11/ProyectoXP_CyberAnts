from src.contracts import IIA
from src.sistema_ruso import CoordenadaUK


class AutomataArsenal:
    SIGMA = {"a", "b", "c", "d", "t"}

    def validar(self, palabra: str) -> bool:
        if not isinstance(palabra, str):
            return False
        w = palabra.strip()
        if not w:
            return False

        estado = "q0"
        for char in w:
            if char not in self.SIGMA:
                return False
            if estado == "q0":
                if char == "a":
                    estado = "q1"
                else:
                    return False
            elif estado == "q1":
                if char == "a":
                    estado = "q2"
                elif char == "b":
                    estado = "q3"
                elif char == "t":
                    estado = "q5"
                else:
                    return False
            elif estado == "q2":
                if char == "a":
                    estado = "q2"
                else:
                    return False
            elif estado == "q3":
                if char == "b":
                    estado = "q3"
                elif char == "c":
                    estado = "q4"
                elif char == "t":
                    estado = "q5"
                else:
                    return False
            elif estado == "q4":
                if char == "d":
                    estado = "q5_pre"
                else:
                    return False
            elif estado == "q5_pre":
                if char == "t":
                    estado = "q5"
                else:
                    return False
            elif estado == "q5":
                if char == "t":
                    estado = "q5"
                else:
                    return False
            else:
                return False

        return estado in ("q1", "q2", "q3", "q5")

    def trazar(self, palabra: str) -> dict:
        if not isinstance(palabra, str) or not palabra.strip():
            return {"palabra": palabra or "", "recorrido": ["q0"], "aceptada": False}

        w = palabra.strip()
        recorrido = ["q0"]
        estado = "q0"
        for char in w:
            if char not in self.SIGMA:
                estado = "q_err"
            elif estado == "q0":
                estado = "q1" if char == "a" else "q_err"
            elif estado == "q1":
                if char == "a":
                    estado = "q2"
                elif char == "b":
                    estado = "q3"
                elif char == "t":
                    estado = "q5"
                else:
                    estado = "q_err"
            elif estado == "q2":
                estado = "q2" if char == "a" else "q_err"
            elif estado == "q3":
                if char == "b":
                    estado = "q3"
                elif char == "c":
                    estado = "q4"
                elif char == "t":
                    estado = "q5"
                else:
                    estado = "q_err"
            elif estado == "q4":
                estado = "q5_pre" if char == "d" else "q_err"
            elif estado == "q5_pre":
                estado = "q5" if char == "t" else "q_err"
            elif estado == "q5":
                estado = "q5" if char == "t" else "q_err"
            else:
                estado = "q_err"

            recorrido.append(estado)
            if estado == "q_err":
                break

        return {
            "palabra": w,
            "recorrido": recorrido,
            "estado_final": estado,
            "aceptada": estado in ("q1", "q2", "q3", "q5"),
        }


class FuentePoder:
    """Fuente de poder recargable y reemplazable bajo asistencia del IIA."""

    def __init__(self, energia: int = 100):
        self.energia = max(0, min(100, int(energia)))
        self.reemplazos = 0

    def consumir(self, cantidad: int) -> bool:
        cantidad = max(0, int(cantidad))
        if self.energia < cantidad:
            return False
        self.energia -= cantidad
        return True

    def recargar(self) -> int:
        self.energia = 100
        return self.energia

    def reemplazar(self) -> int:
        self.reemplazos += 1
        self.energia = 100
        return self.energia


class TurboReactor:
    """Turbo reactor dorsal que permite volar usando energía de la FuentePoder."""

    def __init__(self):
        self.en_vuelo = False

    def activar_vuelo(self, fuente: FuentePoder) -> bool:
        if fuente.consumir(20):
            self.en_vuelo = True
            return True
        self.en_vuelo = False
        return False


class Metralleta:
    """Metralleta equipada en la pata delantera derecha del AntCiberDron."""

    def __init__(self, municion: int = 150):
        self.municion = max(0, int(municion))

    def disparar(self, rafaga: int = 15) -> bool:
        if self.municion < rafaga:
            return False
        self.municion -= rafaga
        return True


class Laser:
    """Láser en la pata delantera izquierda cuya potencia varía según la energía de la FuentePoder."""

    def __init__(self):
        self.potencia = 100

    def sincronizar_potencia(self, fuente: FuentePoder) -> int:
        # La potencia del láser es directamente proporcional a la energía actual (kW)
        self.potencia = int(fuente.energia * 1.5)
        return self.potencia

    def disparar(self, fuente: FuentePoder) -> int:
        potencia_actual = self.sincronizar_potencia(fuente)
        if not fuente.consumir(15):
            self.potencia = 0
            return 0
        self.sincronizar_potencia(fuente)
        return potencia_actual


class ExpertoIdioma:
    """Versión V1 (ANTES DEL REFACTOR): sin validación de caracteres IPA."""

    IDIOMAS_PERMITIDOS = {"ingles", "espanol"}

    def __init__(self, nombre: str, idioma: str):
        nombre_limpio = (nombre or "").strip()
        idioma_norm = (
            (idioma or "")
            .strip()
            .lower()
            .replace("é", "e")
            .replace("ñ", "n")
        )
        if not nombre_limpio:
            raise ValueError("El experto debe tener un nombre válido.")
        if idioma_norm not in self.IDIOMAS_PERMITIDOS:
            raise ValueError("Solo se permiten expertos parlantes de 'ingles' o 'espanol'.")
        self.nombre = nombre_limpio
        self.idioma = idioma_norm


class AntCiberDron(IIA):
    def __init__(self):
        self.automata = AutomataArsenal()
        self.fuente_poder = FuentePoder(energia=100)
        self.turbo_reactor = TurboReactor()
        self.metralleta = Metralleta(municion=150)
        self.laser = Laser()
        self.laser.sincronizar_potencia(self.fuente_poder)
        self.idiomas_entrenados: dict[str, dict] = {
            "ingles": {
                "experto": "Dr. John Miller (Native EN)",
                "lexico": ["target", "deploy", "strike", "abort", "coordinates"],
                "gramatica": "SVO Tactical Command Syntax",
                "fonetica": "/ˈtɑːrɡɪt ˈstraɪk/",
            },
            "espanol": {
                "experto": "Cap. Elena Rostova (Hispano-KGD)",
                "lexico": ["objetivo", "desplegar", "explotar", "coordenada", "arsenal"],
                "gramatica": "Imperativo Militar Sujeto-Verbo-Objeto",
                "fonetica": "/oβxeˈtiβo mi.liˈtaɾ/",
            },
        }

    def buscar(self, tipoArsenal: str) -> bool:
        return self.automata.validar(tipoArsenal)

    def evaluar_coordenadas(self, coordenadas: list[CoordenadaUK]) -> list[dict]:
        resultados = []
        for c in coordenadas:
            accion = self.buscar(c.tipoArsenal)
            traza = self.automata.trazar(c.tipoArsenal)
            resultados.append(
                {
                    "geoposicion": c.geoposicion,
                    "tipoArsenal": c.tipoArsenal,
                    "accion": accion,
                    "accion_str": "true" if accion else "false",
                    "recorrido": " -> ".join(traza["recorrido"]),
                }
            )
        return resultados

    def volar(self) -> bool:
        ok = self.turbo_reactor.activar_vuelo(self.fuente_poder)
        self.laser.sincronizar_potencia(self.fuente_poder)
        return ok

    def disparar_metralleta(self) -> bool:
        return self.metralleta.disparar()

    def disparar_laser(self) -> int:
        return self.laser.disparar(self.fuente_poder)

    def asistir_fuente_poder(self, accion: str = "recargar") -> int:
        if accion == "reemplazar":
            energia = self.fuente_poder.reemplazar()
        else:
            energia = self.fuente_poder.recargar()
        self.laser.sincronizar_potencia(self.fuente_poder)
        return energia

    def entrenar_idioma(
        self, experto: ExpertoIdioma, lexico: list[str], gramatica: str, fonetica: str
    ) -> dict:
        if not isinstance(experto, ExpertoIdioma):
            raise PermissionError(
                "Acceso denegado: solo un ExpertoIdioma autorizado puede entrenar al AntCiberDron."
            )
        lexico_limpio = [w.strip() for w in (lexico or []) if str(w).strip()]
        gramatica_limpia = (gramatica or "").strip()
        fonetica_limpia = (fonetica or "").strip()
        if not lexico_limpio or not gramatica_limpia or not fonetica_limpia:
            raise ValueError("El entrenamiento requiere léxico, gramática y fonética no vacíos.")

        registro = {
            "experto": experto.nombre,
            "lexico": lexico_limpio,
            "gramatica": gramatica_limpia,
            "fonetica": fonetica_limpia,
        }
        self.idiomas_entrenados[experto.idioma] = registro
        return registro
