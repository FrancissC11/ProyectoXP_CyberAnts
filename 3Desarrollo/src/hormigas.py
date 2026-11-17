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


def crear_alimento(nombre: str) -> Alimento:
    """Versión ANTES DEL REFACTOR: fábrica con condicionales if/elif."""
    normalizado = (nombre or "").strip().lower().replace("é", "e").replace("í", "i")
    if normalizado == "nectar" or normalizado == "anectar":
        return ANectar()
    elif normalizado == "carnivoro" or normalizado == "acarnivoro":
        return ACarnivoro()
    else:
        raise ValueError(f"Alimento no permitido para Grupo 2: {nombre}")


class Hormiga(IHormiga, ABC):
    """Versión ANTES DEL REFACTOR: sin Template Method en comer()."""

    def __init__(self, id: int = 1, sexo: str = "Asexual", estado: str = "VIVA"):
        self.id = int(id)
        self.sexo = sexo
        self.estado = estado

    @property
    def tipo(self) -> str:
        return self.__class__.__name__

    def toString(self) -> str:
        return f"{self.tipo} [ID={self.id} | Sexo={self.sexo} | Estado={self.estado}]"

    def __str__(self) -> str:
        return self.toString()


class HSoldado(Hormiga):
    def __init__(self, id: int = 1, sexo: str = "Macho", estado: str = "VIVA"):
        super().__init__(id=id, sexo=sexo, estado=estado)

    # CÓDIGO DUPLICADO #1 (repite la validación de estado y tipo de alimento de HLarva)
    def comer(self, alimento: Alimento) -> bool:
        if self.estado == "MUERTA" or not isinstance(alimento, Alimento):
            self.estado = "MUERTA"
            return False
        if isinstance(alimento, ACarnivoro):
            self.estado = "VIVA"
            return True
        self.estado = "MUERTA"
        return False


class HLarva(Hormiga):
    def __init__(self, id: int = 1, sexo: str = "Asexual", estado: str = "VIVA"):
        super().__init__(id=id, sexo=sexo, estado=estado)

    # CÓDIGO DUPLICADO #2 (repite validación y ramas explícitas)
    def comer(self, alimento: Alimento) -> bool:
        if self.estado == "MUERTA" or not isinstance(alimento, Alimento):
            self.estado = "MUERTA"
            return False
        if isinstance(alimento, ANectar):
            self.estado = "VIVA"
            return True
        if isinstance(alimento, ACarnivoro):
            self.__class__ = HSoldado
            if self.sexo == "Asexual":
                self.sexo = "Macho"
            self.estado = "VIVA"
            return True
        self.estado = "MUERTA"
        return False


def reconstruir_hormiga(id: int, tipo: str, sexo: str, estado: str) -> Hormiga:
    clases = {
        "HLarva": HLarva,
        "HSoldado": HSoldado,
    }
    cls = clases.get(tipo, HLarva)
    return cls(id=id, sexo=sexo, estado=estado)


class HormigueroVirtual:
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
        for h in self.hormigas:
            if h.id == id_hormiga:
                return h
        return None

    def alimentar_hormiga(self, id_hormiga: int, alimento: Alimento) -> bool:
        hormiga = self.obtener_hormiga(id_hormiga)
        if hormiga is None:
            raise KeyError(f"No existe la hormiga con id={id_hormiga}")
        return hormiga.comer(alimento)
