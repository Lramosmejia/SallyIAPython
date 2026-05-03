from ..services.estudiante_service import EstudianteService

# ── Estado en memoria por usuario ─────────────────────────────────────────────
# Clave: numero de WhatsApp  |  Valor: estado actual de la conversacion
_estados_usuarios: dict[str, str] = {}

# Palabras que inician el flujo de consulta de estudiante
PALABRAS_CONSULTA: frozenset[str] = frozenset({"estado", "consultar"})


class ChatbotService:
    """Orquesta el flujo conversacional del chatbot."""

    def __init__(self):
        self.estudiante_service = EstudianteService()

    # ─────────────────────────────────────────────────────────────────────────
    # MÉTODO PRINCIPAL
    # ─────────────────────────────────────────────────────────────────────────

    def procesar_mensaje(self, data: dict) -> str | None:
        """
        Extrae número, tipo y contenido del payload de Meta,
        aplica el flujo conversacional y retorna la respuesta como texto,
        o None si el payload no es procesable.
        """
        try:
            entry  = data['entry'][0]['changes'][0]['value']
            msg    = entry['messages'][0]
            numero = msg['from']
            tipo   = msg.get('type', 'unknown')

            contenido = self._extraer_contenido(tipo, msg)

            return self._flujo(numero, contenido)

        except (KeyError, IndexError):
            return None

    # ─────────────────────────────────────────────────────────────────────────
    # EXTRACCIÓN DE CONTENIDO SEGÚN TIPO
    # ─────────────────────────────────────────────────────────────────────────

    def _extraer_contenido(self, tipo: str, msg: dict) -> str:
        """Soporta mensajes de texto, button_reply y list_reply."""

        if tipo == 'text':
            return msg.get('text', {}).get('body', '').lower().strip()

        if tipo == 'interactive':
            interactive = msg.get('interactive', {})

            if 'button_reply' in interactive:
                return interactive['button_reply'].get('id', '').lower().strip()

            if 'list_reply' in interactive:
                return interactive['list_reply'].get('id', '').lower().strip()

        return 'no_soportado'

    # ─────────────────────────────────────────────────────────────────────────
    # FLUJO CONVERSACIONAL
    # ─────────────────────────────────────────────────────────────────────────

    def _flujo(self, numero: str, contenido: str) -> str:

        estado_actual = _estados_usuarios.get(numero, 'menu')

        # ── El usuario está esperando que se le pida su identificación ────────
        if estado_actual == 'esperando_identificacion':
            return self._validar_identificacion(numero, contenido)

        # ── El usuario pide consultar su estado académico ─────────────────────
        if contenido in PALABRAS_CONSULTA:
            _estados_usuarios[numero] = 'esperando_identificacion'
            return (
                "Por favor ingresa tu *número de identificación*.\n\n"
                "⚠️ Sin puntos ni espacios. Ejemplo: *1234567890*"
            )

        # ── Contenido no reconocido en este servicio ──────────────────────────
        return None  # El caller puede delegar a MessageService

    # ─────────────────────────────────────────────────────────────────────────
    # VALIDACIÓN DE IDENTIFICACIÓN Y RESPUESTA CON DATOS DEL ESTUDIANTE
    # ─────────────────────────────────────────────────────────────────────────

    def _validar_identificacion(self, numero: str, identificacion: str) -> str:

        # Resetear estado sin importar el resultado
        _estados_usuarios[numero] = 'menu'

        estudiante = self.estudiante_service.validar_estudiante(identificacion)

        if not estudiante:
            return (
                "❌ No encontré ningún estudiante con la identificación "
                f"*{identificacion}*.\n\n"
                "Verifica el número e intenta de nuevo escribiendo *consultar*."
            )

        return (
            f"✅ *Información académica de {estudiante.nombre}*\n\n"
            f"📋 *Estado académico:* {estudiante.estado_academico or 'No disponible'}\n"
            f"📚 *Semestre:* {estudiante.semestre or 'No disponible'}\n\n"
            f"🕐 *Horario:*\n{estudiante.horario or 'No disponible'}\n\n"
            f"👨‍🏫 *Docentes:*\n{estudiante.docentes or 'No disponible'}"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # UTILIDADES DE ESTADO
    # ─────────────────────────────────────────────────────────────────────────

    def obtener_estado(self, numero: str) -> str:
        """Retorna el estado actual de la conversación de un usuario."""
        return _estados_usuarios.get(numero, 'menu')

    def resetear_estado(self, numero: str) -> None:
        """Fuerza el estado de un usuario a 'menu'."""
        _estados_usuarios[numero] = 'menu'