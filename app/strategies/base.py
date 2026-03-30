from abc import ABC, abstractmethod


class MensajeStrategy(ABC):


    @abstractmethod
    def soporta(self, tipo: str) -> bool:
        pass

    @abstractmethod
    def extraer_contenido(self, msg: dict) -> str:
        pass