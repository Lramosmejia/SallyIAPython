
from __future__ import annotations

from ..repositories.log_repository import LogRepository
from ..integrations.whatsapp_adapter import WhatsAppAdapter
from ..strategies.registry import StrategyRegistry

# Palabras de fallback (cuando chatbot retorna None y el contenido es desconocido)
MENSAJE_FALLBACK = (
    "No entendi tu mensaje.\n\n"
    "Escribe *hola* o *menu* para ver las opciones disponibles."
)


class MessageService:

    def __init__(self) -> None:
        self.repository = LogRepository()
        self.adapter    = WhatsAppAdapter()
        self.registry   = StrategyRegistry()

    # -------------------------------------------------------------------------
    # PUNTO DE ENTRADA
    # -------------------------------------------------------------------------

    def procesar_webhook(
        self,
        data: dict,
        respuesta_externa: list[dict] | None = None,
    ) -> None:

        try:
            entry     = data["entry"][0]["changes"][0]["value"]
            msg       = entry["messages"][0]
            numero    = msg["from"]
            tipo      = msg.get("type", "unknown")

            strategy  = self.registry.resolver(tipo)
            contenido = strategy.extraer_contenido(msg) if strategy else "no_soportado"

            # Log siempre — independientemente de quien responda
            self.repository.guardar(f"{numero}: {contenido}")

            # Despachar respuesta
            if respuesta_externa is not None:
                self._enviar_lista(numero, respuesta_externa)
            else:
                self._fallback(numero)

        except (KeyError, IndexError) as e:
            print(f"[MessageService] Payload no procesable (status update?): {e}")
        except Exception as e:
            print(f"[MessageService] Error inesperado: {e}")

    # -------------------------------------------------------------------------
    # ENVIO DE RESPUESTAS
    # -------------------------------------------------------------------------

    def _enviar_lista(self, numero: str, mensajes: list[dict]) -> None:
        """Itera y envía cada mensaje de la lista usando el adaptador correcto."""
        for msg in mensajes:
            try:
                self._enviar_uno(numero, msg)
            except Exception as e:
                print(f"[MessageService] Error al enviar mensaje a {numero}: {e}")

    def _enviar_uno(self, numero: str, msg: dict) -> None:
        """Despacha un dict de mensaje al metodo correcto del adaptador."""
        tipo = msg.get("type")

        if tipo == "text":
            self.adapter.enviar_texto(numero, msg["body"])

        elif tipo == "buttons":
            self.adapter.enviar_botones(
                numero=numero,
                cuerpo=msg["body"],
                botones=msg["buttons"],
            )

        elif tipo == "list":
            self.adapter.enviar_lista(
                numero=numero,
                cuerpo=msg["body"],
                boton_texto=msg.get("button_text", "Ver opciones"),
                secciones=msg["sections"],
            )

        else:
            print(f"[MessageService] Tipo de mensaje desconocido: {tipo!r}")

    def _fallback(self, numero: str) -> None:
        """Respuesta cuando ChatbotService no reconocio el contenido."""
        try:
            self.adapter.enviar_texto(numero, MENSAJE_FALLBACK)
        except Exception as e:
            print(f"[MessageService] Error en fallback a {numero}: {e}")