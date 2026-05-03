from ..repositories.log_repository import LogRepository
from ..integrations.whatsapp_adapter import WhatsAppAdapter
from ..strategies.registry import StrategyRegistry


RESPUESTAS: dict[str, str] = {
    "matriculas": (
        "*Información de Matrículas*\n\n"
        "• Fechas de inscripción: 1-15 de cada mes\n"
        "• Costo por crédito: consulta en caja\n"
        "• Requisitos: paz y salvo + carné vigente\n\n"
        " Más info: www.universidad.edu/matriculas"
    ),
    "horarios": (
        "*Consulta de Horarios*\n\n"
        "Ingresa al portal estudiantil para ver tu horario personalizado:\n"
        "www.universidad.edu/horarios\n\n"
        "Usuario: tu número de documento\n"
        "Clave: fecha de nacimiento (DDMMAAAA)"
    ),
    "soporte": (
        "🛠 *Soporte Técnico*\n\n"
        "soporte@universidad.edu\n"
        "(601) 123-4567 ext. 200\n"
        "Lunes a Viernes: 8:00am - 5:00pm\n\n"
        "También puedes abrir un ticket en:\n"
        "soporte.universidad.edu"
    ),
}

# Botones del menú principal 
MENU_BOTONES: list[dict] = [
    {"id": "matriculas", "title": " Matrículas"},
    {"id": "horarios",   "title": " Horarios"},
    {"id": "soporte",    "title": " Soporte"},
]

# Palabras clave que activan el menú principal
PALABRAS_MENU: frozenset[str] = frozenset({
    "hola", "menu", "menú", "inicio", "start",
    "ayuda", "help", "opciones", "hi", "hello",
})


class MessageService:


    def __init__(self):
        self.repository = LogRepository()
        self.adapter    = WhatsAppAdapter()
        self.registry   = StrategyRegistry()

    def procesar_webhook(self, data: dict, respuesta_externa: str | None) -> None:

        try:
            # Extraer el mensaje del payload de Meta (estructura fija)
            entry  = data['entry'][0]['changes'][0]['value']
            msg    = entry['messages'][0]
            numero = msg['from']
            tipo   = msg.get('type', 'unknown')

            # Resolver strategy y extraer contenido
            strategy  = self.registry.resolver(tipo)
            contenido = strategy.extraer_contenido(msg) if strategy else 'no_soportado'

            # Log en BD
            self.repository.guardar(f"{numero}: {contenido}")

            # Generar respuesta
            if respuesta_externa is not None:
                self.adapter.enviar_texto(numero, respuesta_externa)
                return
            
            self._responder(numero, contenido)

        except (KeyError, IndexError) as e:
            # Payload inesperado (notificación de estado, mensajes de sistema, etc.)
            print(f"[MessageService] Payload no procesable (puede ser status update): {e}")
        except Exception as e:
            print(f"[MessageService] Error inesperado: {e}")

    def _responder(self, numero: str, contenido: str) -> None:

        try:
            if contenido in PALABRAS_MENU:
                self.adapter.enviar_botones(
                    numero=numero,
                    cuerpo=(
                        " ¡Hola! Soy *Sally*, tu asistente universitaria.\n"
                        "¿En qué puedo ayudarte hoy?"
                    ),
                    botones=MENU_BOTONES,
                )

            elif contenido in RESPUESTAS:
                self.adapter.enviar_texto(numero, RESPUESTAS[contenido])

            else:
                self.adapter.enviar_texto(
                    numero,
                    (
                        " No entendí tu mensaje.\n\n"
                        "Escribe *menu* o *hola* para ver las opciones disponibles."
                    )
                )

        except Exception as e:
            print(f"[MessageService] Error al enviar respuesta a {numero}: {e}")