from .base import MensajeStrategy
from .text_strategy import TextMessageStrategy
from .interactive_strategy import InteractiveStrategy


class StrategyRegistry:
    

    def __init__(self):
        self._strategies: list[MensajeStrategy] = []
        self._registrar_defaults()

    def _registrar_defaults(self) -> None:
        
        self.registrar(TextMessageStrategy())
        self.registrar(InteractiveStrategy())

    def registrar(self, strategy: MensajeStrategy) -> None:
       
        self._strategies.append(strategy)

    def resolver(self, tipo: str) -> MensajeStrategy | None:
       
        for strategy in self._strategies:
            if strategy.soporta(tipo):
                return strategy
        return None

    def tipos_soportados(self) -> list[str]:
        
        return [s.__class__.__name__ for s in self._strategies]