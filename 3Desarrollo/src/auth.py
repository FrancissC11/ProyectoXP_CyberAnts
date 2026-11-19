from dataclasses import dataclass


@dataclass(frozen=True)
class MiembroEquipo:
    orden: int
    cedula: str
    nombre: str
    username: str
    aliases: tuple[str, ...]
    rol_xp: str
    rol_hormiguero: str

    @property
    def ultimo_digito(self) -> str:
        return self.cedula[-1]

    @property
    def coordenada_asignada(self) -> str:
        return f"Coord-0{self.ultimo_digito}"


EQUIPO_CYBERANTS: tuple[MiembroEquipo, ...] = (
    MiembroEquipo(
        orden=1,
        cedula="0402132500",
        nombre="Chuga Juan",
        username="jchuga",
        aliases=("jchuga", "juan", "0402132500"),
        rol_xp="Programador (Pareja 1) + Tracker",
        rol_hormiguero="Hormiga Soldado",
    ),
    MiembroEquipo(
        orden=2,
        cedula="1755580402",
        nombre="Camino Emilio",
        username="ecamino",
        aliases=("ecamino", "emilio", "1755580402"),
        rol_xp="Coach XP + Gestor",
        rol_hormiguero="Hormiga Exploradora",
    ),
    MiembroEquipo(
        orden=3,
        cedula="0503855330",
        nombre="Casa Fernando",
        username="fcasa",
        aliases=("fcasa", "fernando", "0503855330"),
        rol_xp="Programador (Pareja 1) + Tester",
        rol_hormiguero="Hormiga Obrera",
    ),
    MiembroEquipo(
        orden=4,
        cedula="1726339151",
        nombre="Carcelén Josué",
        username="jcarcelen",
        aliases=("jcarcelen", "josue", "1726339151"),
        rol_xp="Programador (Pareja 2) + Tester",
        rol_hormiguero="Hormiga Centinela",
    ),
    MiembroEquipo(
        orden=5,
        cedula="1729044121",
        nombre="Carrera Fernando",
        username="fcarrera",
        aliases=("fcarrera", "stalin", "carrera", "1729044121"),
        rol_xp="Programador (Pareja 2)",
        rol_hormiguero="Hormiga Nodriza",
    ),
    MiembroEquipo(
        orden=6,
        cedula="1005444912",
        nombre="Cartagena Franciss",
        username="fcartagena",
        aliases=("fcartagena", "franciss", "1005444912"),
        rol_xp="Cliente",
        rol_hormiguero="Hormiga Reina",
    ),
)


class AuthService:
    """
    Servicio de autenticación KGD con máximo 3 intentos fallidos.
    Acepta a los 6 integrantes del equipo y al profesor ('patmic' / '123').
    """

    MAX_INTENTOS = 3
    GRUPO_NUMERO = 2
    GRUPO_NOMBRE = "Colonia CyberAnts"

    def __init__(self):
        self.intentos_fallidos = 0
        self.bloqueado = False
        self.usuario_autenticado: str | None = None

    def reiniciar_intentos(self) -> None:
        self.intentos_fallidos = 0
        self.bloqueado = False
        self.usuario_autenticado = None

    @property
    def intentos_restantes(self) -> int:
        return max(0, self.MAX_INTENTOS - self.intentos_fallidos)

    def autenticar(self, usuario: str | None, password: str | None) -> dict:
        if self.bloqueado:
            return {
                "exito": False,
                "bloqueado": True,
                "intentos_restantes": 0,
                "mensaje": "ACCESO BLOQUEADO: Se superó el límite máximo de 3 intentos.",
            }

        user_clean = (usuario or "").strip().lower()
        pass_clean = (password or "").strip()

        if not user_clean or not pass_clean:
            return self._registrar_fallo("Credenciales vacías o incompletas.")

        # 1. Validar profesor patmic / 123
        if user_clean == "patmic" and pass_clean == "123":
            self.intentos_fallidos = 0
            self.usuario_autenticado = "patmic (Profesor Evaluador)"
            return {
                "exito": True,
                "bloqueado": False,
                "intentos_restantes": self.MAX_INTENTOS,
                "usuario": self.usuario_autenticado,
                "mensaje": f"[+] TEAM [{self.GRUPO_NUMERO}]: {self.GRUPO_NOMBRE}",
            }

        # 2. Validar a cualquiera de los 6 integrantes (password '123' o su cédula)
        for m in EQUIPO_CYBERANTS:
            if user_clean in m.aliases and pass_clean in ("123", m.cedula):
                self.intentos_fallidos = 0
                self.usuario_autenticado = f"{m.nombre} ({m.cedula})"
                return {
                    "exito": True,
                    "bloqueado": False,
                    "intentos_restantes": self.MAX_INTENTOS,
                    "usuario": self.usuario_autenticado,
                    "mensaje": f"[+] TEAM [{self.GRUPO_NUMERO}]: {self.GRUPO_NOMBRE}",
                }

        return self._registrar_fallo("Usuario o contraseña incorrectos.")

    def _registrar_fallo(self, motivo: str) -> dict:
        self.intentos_fallidos += 1
        if self.intentos_fallidos >= self.MAX_INTENTOS:
            self.bloqueado = True
            return {
                "exito": False,
                "bloqueado": True,
                "intentos_restantes": 0,
                "mensaje": (
                    f"{motivo} ACCESO BLOQUEADO tras {self.MAX_INTENTOS} intentos fallidos."
                ),
            }
        return {
            "exito": False,
            "bloqueado": False,
            "intentos_restantes": self.intentos_restantes,
            "mensaje": f"{motivo} Intentos restantes: {self.intentos_restantes}.",
        }

    def formatear_ficha_equipo(self) -> str:
        lineas = [f"[+] TEAM [{self.GRUPO_NUMERO}]: {self.GRUPO_NOMBRE}"]
        for m in EQUIPO_CYBERANTS:
            lineas.append(f"  • Alumno {m.orden}: {m.cedula} | {m.nombre}")
        return "\n".join(lineas)
