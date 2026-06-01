from __future__ import annotations

from ..services.estudiante_service import EstudianteService
from ..state.conversation_state import conversation_state
from ..flows.conversation_flow import (
    TRIGGERS_MENU_PRINCIPAL,
    TRIGGERS_ESTADO_ACADEMICO,
    MAIN_MENU,
    SUBMENUS,
    CONTENT,
    FOLLOW_UP,
    ENCUESTA,
    ENCUESTA_RESPUESTAS,
    SUBMENU_IDS,
    CONTENT_IDS,
    ENCUESTA_IDS,
)


class ChatbotService:
    """Orquesta el flujo conversacional del chatbot."""

    def __init__(self) -> None:
        self.estudiante_service = EstudianteService()
        self.state = conversation_state

    # ─────────────────────────────────────────────────────────────────────────
    # MÉTODO PRINCIPAL
    # ─────────────────────────────────────────────────────────────────────────

    def procesar_mensaje(self, data: dict) -> list[dict] | None:
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
            
            print(f"[ChatbotService] {numero} | estado= {self.state.get_state(numero)} | contenido= {contenido!r}")

            return self._resolver_flujo(numero, contenido)

        except (KeyError, IndexError):
            return None

    # ─────────────────────────────────────────────────────────────────────────
    # EXTRACCIÓN DE CONTENIDO SEGÚN TIPO
    # ─────────────────────────────────────────────────────────────────────────

    def _extraer_contenido(self, tipo: str, msg: dict) -> str:
        """Soporta mensajes de texto, button_reply y list_reply."""

        if tipo == "text":
            return msg.get("text", {}).get("body", "").lower().strip()

        if tipo == "interactive":
            interactive = msg.get("interactive", {})

            if "button_reply" in interactive:
                return interactive["button_reply"].get("id", "").lower().strip()

            if "list_reply" in interactive:
                return interactive["list_reply"].get("id", "").lower().strip()

        return "no_soportado"

    # ─────────────────────────────────────────────────────────────────────────
    # FLUJO CONVERSACIONAL
    # ─────────────────────────────────────────────────────────────────────────

    def _resolver_flujo(self, numero: str, contenido: str) -> list[dict] | None:

        estado_actual = self.state.get_state(numero)

        #1. Triggers del menú principal — SIEMPRE tienen prioridad
        if contenido in TRIGGERS_MENU_PRINCIPAL:
            self.state.set_state(numero, "in_main_menu")
            return (
                [MAIN_MENU]
            )

        #2. Navegacion a submenú — prioridad sobre estados especiales
        if contenido in SUBMENU_IDS:
            self.state.set_state(numero, f"in_{contenido}")
            return [SUBMENUS[contenido]]

        #3. Respuestas a opciones específicas de submenú
        if contenido in CONTENT_IDS:
            self.state.set_state(numero, "in_followup")
            return[{
                "type": "text", "body": CONTENT[contenido]},
                FOLLOW_UP]

        #4. Trigger de estado académico
        if contenido in TRIGGERS_ESTADO_ACADEMICO:
            self.state.set_state(numero, "esperando_identificacion")
            return [{
                "type": "text",
                "body":("Por favor ingresa tu *numero de identificación*.\n\n" 
                "Sin puntos ni espacios. Ejemplo: *1234567890*"),
            }]

        #5. Estado especial: esperando identificación (solo captura texto libre)
        if estado_actual == "esperando_identificacion":
            return self._flujo_identificacion(numero, contenido)
        
        # 6. Finalizar → encuesta
        if contenido == "finalizar":
            self.state.set_state(numero, "in_encuesta")
            return [ENCUESTA]

        # 7. Respuestas de la encuesta
        if contenido in ENCUESTA_IDS:
            self.state.reset(numero)
            return [{"type": "text", "body": ENCUESTA_RESPUESTAS[contenido]}]   
        
        #8. Respuesta por defecto    
        return None  

    # ─────────────────────────────────────────────────────────────────────────
    # VALIDACIÓN DE IDENTIFICACIÓN Y RESPUESTA CON DATOS DEL ESTUDIANTE
    # ─────────────────────────────────────────────────────────────────────────

    def _flujo_identificacion(self, numero: str, identificacion: str) -> list[dict]:
        self.state.set_state(numero, "in_followup")

        estudiante = self.estudiante_service.validar_estudiante(identificacion)

        if not estudiante:
            return [
                {
                    "type": "text",
                    "body": (
                        f"No encontre ningun estudiante con la identificacion "
                        f"*{identificacion}*.\n\nVerifica el numero e intentalo de nuevo."
                    ),
                },
                FOLLOW_UP,
            ]

        return [
            {
                "type": "text",
                "body": (
                    f"Informacion Academica\n\n"
                    f"Estudiante: {estudiante.nombre}\n"
                    f"ID: {estudiante.numero_identificacion}\n\n"
                    f"Estado academico: {estudiante.estado_academico or 'No disponible'}\n"
                    f"Semestre: {estudiante.semestre or 'No disponible'}\n\n"
                    f"Horario:\n{estudiante.horario or 'No disponible'}\n\n"
                    f"Docentes:\n{estudiante.docentes or 'No disponible'}"
                ),
            },
            FOLLOW_UP,
        ]

    # -------------------------------------------------------------------------
    # UTILIDADES PUBLICAS
    # -------------------------------------------------------------------------

    def obtener_estado(self, numero: str) -> str:
        return self.state.get_state(numero)

    def resetear_estado(self, numero: str) -> None:
        self.state.reset(numero)