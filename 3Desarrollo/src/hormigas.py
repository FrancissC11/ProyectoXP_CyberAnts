from abc import ABC
from src.contracts import IHormiga


class Alimento(ABC):
    """Clase abstracta Alimento según el diagrama de clases."""

    def __init__(self, nombre: str):
        self.nombre = nombre

    def toString(self) -> str:
        return self.nombre

    def __str__(self) -> str:
        return self.toString()


class ANectar(Alimento):
    def __init__(self):
        super().__init__("Néctar")


class ACarnivoro(Alimento):
    def __init__(self):
        super().__init__("Carnívoro")


MAPA_ALIMENTOS: dict[str, type[Alimento]] = {
    "nectar": ANectar,
    "anectar": ANectar,
    "carnivoro": ACarnivoro,
    "acarnivoro": ACarnivoro,
}


def crear_alimento(nombre: str) -> Alimento:
    """Fábrica simple de alimentos del Grupo 2 (Néctar y Carnívoro)."""
    normalizado = (nombre or "").strip().lower().replace("é", "e").replace("í", "i")
    if normalizado not in MAPA_ALIMENTOS:
        raise ValueError(f"Alimento no permitido para Grupo 2: {nombre}")
    return MAPA_ALIMENTOS[normalizado]()


class Hormiga(IHormiga, ABC):
    """
    Clase abstracta Hormiga refactorizada con Template Method y ALIMENTO_VITAL.
    Implementa IHormiga.comer(Alimento) sin duplicación entre subclases.
    """

    ALIMENTO_VITAL: type[Alimento] = ANectar
    SEXO_POR_DEFECTO: str = "Asexual"

    def __init__(self, id: int = 1, sexo: str | None = None, estado: str = "VIVA"):
        self.id = int(id)
        self.sexo = sexo or self.SEXO_POR_DEFECTO
        self.estado = estado

    @property
    def tipo(self) -> str:
        return self.__class__.__name__

    def _validar_estado_y_alimento(self, alimento: Alimento) -> bool:
        if self.estado == "MUERTA" or not isinstance(alimento, Alimento):
            self.estado = "MUERTA"
            return False
        return True

    def comer(self, alimento: Alimento) -> bool:
        if not self._validar_estado_y_alimento(alimento):
            return False
        if isinstance(alimento, self.ALIMENTO_VITAL):
            self.estado = "VIVA"
            return True
        self.estado = "MUERTA"
        return False

    def toString(self) -> str:
        return f"{self.tipo} [ID={self.id} | Sexo={self.sexo} | Estado={self.estado}]"

    def __str__(self) -> str:
        return self.toString()


class HSoldado(Hormiga):
    """Hormiga Soldado (Grupo 2): vive exclusivamente comiendo Carnívoro."""

    ALIMENTO_VITAL = ACarnivoro
    SEXO_POR_DEFECTO = "Macho"


class HLarva(Hormiga):
    """
    Toda hormiga del Grupo 2 nace como HLarva y vive comiendo Néctar.
    Si come Carnívoro, evoluciona a HSoldado.
    """

    ALIMENTO_VITAL = ANectar
    SEXO_POR_DEFECTO = "Asexual"

    def comer(self, alimento: Alimento) -> bool:
        if not self._validar_estado_y_alimento(alimento):
            return False

        if isinstance(alimento, ANectar):
            self.estado = "VIVA"
            return True

        if isinstance(alimento, ACarnivoro):
            self.__class__ = HSoldado
            if self.sexo == "Asexual":
                self.sexo = HSoldado.SEXO_POR_DEFECTO
            self.estado = "VIVA"
            return True

        self.estado = "MUERTA"
        return False


def reconstruir_hormiga(id: int, tipo: str, sexo: str, estado: str) -> Hormiga:
    clases: dict[str, type[Hormiga]] = {
        "HLarva": HLarva,
        "HSoldado": HSoldado,
    }
    cls = clases.get(tipo, HLarva)
    return cls(id=id, sexo=sexo, estado=estado)


class HormigueroVirtual:
    """Gestiona la colonia de hormigas del Grupo 2 (HLarva -> HSoldado)."""

    def __init__(self):
        self.hormigas: list[Hormiga] = []
        self._next_id = 1

    def crear_hormiga(self, sexo: str = "Asexual") -> HLarva:
        sexo_limpio = (sexo or "Asexual").strip() or "Asexual"
        nueva = HLarva(id=self._next_id, sexo=sexo_limpio, estado="VIVA")
        self._next_id += 1
        self.hormigas.append(nueva)
        return nueva

    def obtener_hormiga(self, id_hormiga: int) -> Hormiga | None:
        return next((h for h in self.hormigas if h.id == id_hormiga), None)

    def alimentar_hormiga(self, id_hormiga: int, alimento: Alimento) -> bool:
        hormiga = self.obtener_hormiga(id_hormiga)
        if hormiga is None:
            raise KeyError(f"No existe la hormiga con id={id_hormiga}")
        return hormiga.comer(alimento)
