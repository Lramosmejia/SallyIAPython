from .base import MensajeStrategy


class TextMessageStrategy(MensajeStrategy):
    

    def soporta(self, tipo: str) -> bool:
        return tipo == 'text'

    def extraer_contenido(self, msg: dict) -> str:

        return msg.get('text', {}).get('body', '').lower().strip()