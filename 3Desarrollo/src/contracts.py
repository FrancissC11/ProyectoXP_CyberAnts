from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.hormigas import Alimento


class IHormiga(ABC):
    """Interfaz IHormiga del paquete pkAntCiberDronContract."""

    @abstractmethod
    def comer(self, alimento: "Alimento") -> bool:
        """Alimenta a la hormiga y devuelve True si sobrevive, False si muere o rechaza."""
        raise NotImplementedError


class IIA(ABC):
    """Interfaz IIA (Inteligencia Artificial) del paquete pkAntCiberDronContract."""

    @abstractmethod
    def buscar(self, tipoArsenal: str) -> bool:
        """Evalúa si la cadena tipoArsenal pertenece al lenguaje del autómata para explotar la bomba."""
        raise NotImplementedError


class Utility:
    """Clase utilitaria para la animación de carga exigida por el sistema ruso."""

    FRAMES = ("\\", "|", "/", "-")

    @classmethod
    def generar_pasos_loading(cls) -> list[str]:
        """Devuelve la secuencia de pasos de carga desde 10% hasta 100% usando \\ | / -."""
        pasos = []
        for idx, pct in enumerate((10, 35, 65, 90)):
            simbolo = cls.FRAMES[idx % len(cls.FRAMES)]
            pasos.append(f"{simbolo} {pct}%")
        pasos.append("100%")
        return pasos
