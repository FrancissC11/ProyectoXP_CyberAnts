from src.contracts import IIA
from src.sistema_ruso import CoordenadaUK


class AutomataArsenal:
    """
    Autómata Finito Determinista A = (Q, Σ, δ, q0, F) del Grupo 2:
      - Últimos dígitos de las 6 cédulas: 0, 2, 0, 1, 1, 2 (Coord-00/01: a+, Coord-02: ab*)
      - Extensión táctica sobre {a, b, t} y abcdt+: acepta combinaciones con a, b y t.
    Lenguaje reconocido: L = { a+, ab*, ab*t+, abcdt+ } sobre Σ = {a, b, c, d, t}.
    """

    Q = {"q0", "q1", "q2", "q3", "q4", "q5_pre", "q5", "q_err"}
    SIGMA = {"a", "b", "c", "d", "t"}
    Q0 = "q0"
    F = {"q1", "q2", "q3", "q5"}

    DELTA = {
        "q0":     {"a": "q1",    "b": "q_err", "c": "q_err", "d": "q_err",  "t": "q_err"},
        "q1":     {"a": "q2",    "b": "q3",    "c": "q_err", "d": "q_err",  "t": "q5"},
        "q2":     {"a": "q2",    "b": "q_err", "c": "q_err", "d": "q_err",  "t": "q_err"},
        "q3":     {"a": "q_err", "b": "q3",    "c": "q4",    "d": "q_err",  "t": "q5"},
        "q4":     {"a": "q_err", "b": "q_err", "c": "q_err", "d": "q5_pre", "t": "q_err"},
        "q5_pre": {"a": "q_err", "b": "q_err", "c": "q_err", "d": "q_err",  "t": "q5"},
        "q5":     {"a": "q_err", "b": "q_err", "c": "q_err", "d": "q_err",  "t": "q5"},
        "q_err":  {"a": "q_err", "b": "q_err", "c": "q_err", "d": "q_err",  "t": "q_err"},
    }

    def validar(self, palabra: str) -> bool:
        """Evalúa si la palabra pertenece a L = { a+, ab*, ab*t+, abcdt+ }."""
        if not isinstance(palabra, str):
            return False
        w = palabra.strip()
        if not w:
            return False

        estado = self.Q0
        for char in w:
            if char not in self.SIGMA:
                return False
            estado = self.DELTA[estado][char]
            if estado == "q_err":
                return False

        return estado in self.F

    def trazar(self, palabra: str) -> dict:
        """Devuelve la traza paso a paso de estados para mostrar en el panel táctico."""
        if not isinstance(palabra, str) or not palabra.strip():
            return {"palabra": palabra or "", "recorrido": ["q0"], "aceptada": False}

        w = palabra.strip()
        recorrido = [self.Q0]
        estado = self.Q0
        for char in w:
            if char not in self.SIGMA:
                estado = "q_err"
            else:
                estado = self.DELTA[estado][char]
            recorrido.append(estado)
            if estado == "q_err":
                break

        return {
            "palabra": w,
            "recorrido": recorrido,
            "estado_final": estado,
            "aceptada": estado in self.F,
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
    """Experto parlante autorizado para entrenar inglés o español en el AntCiberDron."""

    IDIOMAS_PERMITIDOS = {"ingles", "espanol"}
    VOCALES_IPA = set("aeiouɑæɐɒɛɜɞəɨɪɔøœɶʊʌʏy")
    CONSONANTES_Y_MARCAS_IPA = set("pbtdkgɡfvθðszʃʒhmnŋlrɾɹjwβɣʎɲxʧʤʔˈˌː. ")
    CARACTERES_IPA_VALIDOS = VOCALES_IPA | CONSONANTES_Y_MARCAS_IPA

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

    @classmethod
    def validar_fonetica_ipa(cls, fonetica: str) -> str:
        """Valida que la transcripción esté entre /.../ o [...] y use solo caracteres IPA con al menos una vocal."""
        texto = (fonetica or "").strip()
        for prefijo in ("IPA ", "AFI ", "ipa ", "afi "):
            if texto.startswith(prefijo):
                texto = texto[len(prefijo):].strip()

        es_barra = len(texto) >= 3 and texto.startswith("/") and texto.endswith("/")
        es_corchete = len(texto) >= 3 and texto.startswith("[") and texto.endswith("]")
        if not (es_barra or es_corchete):
            raise ValueError(
                "Fonética inválida: debe ir entre /.../ o [...] usando caracteres del Alfabeto Fonético Internacional (IPA)."
            )

        cuerpo = texto[1:-1].strip()
        if not cuerpo or any(ch not in cls.CARACTERES_IPA_VALIDOS for ch in cuerpo):
            raise ValueError(
                "Fonética inválida: contiene caracteres fuera del Alfabeto Fonético Internacional (IPA)."
            )
        if not any(ch in cls.VOCALES_IPA for ch in cuerpo):
            raise ValueError(
                "Fonética inválida: la transcripción IPA debe incluir al menos una vocal fonética."
            )
        return texto


class AntCiberDron(IIA):
    """
    Exoesqueleto táctico AntCiberDron que integra el autómata de destrucción de arsenal,
    extremidades armadas (metralleta derecha, láser izquierdo), turbo reactor, fuente de
    poder asistida por IIA y módulo de entrenamiento de idiomas (inglés y español).
    """

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
        """Implementación de IIA.buscar(tipoArsenal): devuelve True si la bomba debe explotar."""
        return self.automata.validar(tipoArsenal)

    def evaluar_coordenadas(self, coordenadas: list[CoordenadaUK]) -> list[dict]:
        """Evalúa cada coordenada con el autómata y devuelve el reporte táctico."""
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
        """Asistencia del IIA para recargar o reemplazar la fuente de poder."""
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
        if not lexico_limpio or not gramatica_limpia:
            raise ValueError("El entrenamiento requiere léxico y gramática no vacíos.")

        fonetica_limpia = ExpertoIdioma.validar_fonetica_ipa(fonetica)

        registro = {
            "experto": experto.nombre,
            "lexico": lexico_limpio,
            "gramatica": gramatica_limpia,
            "fonetica": fonetica_limpia,
        }
        self.idiomas_entrenados[experto.idioma] = registro
        return registro
