from .base import MensajeStrategy


class InteractiveStrategy(MensajeStrategy):
    

    def soporta(self, tipo: str) -> bool:
        return tipo == 'interactive'

    def extraer_contenido(self, msg: dict) -> str:

        interactive = msg.get('interactive', {})

        if 'button_reply' in interactive:
            return interactive['button_reply'].get('id', 'no_soportado')

        if 'list_reply' in interactive:
            return interactive['list_reply'].get('id', 'no_soportado')

        return 'no_soportado'