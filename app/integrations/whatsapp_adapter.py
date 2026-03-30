import requests
from flask import current_app


class WhatsAppAdapter:

    def __init__(self):
        self._session = requests.Session()

    def _url(self) -> str:
        phone_id = current_app.config['WHATSAPP_PHONE_NUMBER_ID']
        base = current_app.config['WHATSAPP_API_URL']
        return f"{base}/{phone_id}/messages"

    def _headers(self) -> dict:
        token = current_app.config['WHATSAPP_ACCESS_TOKEN']
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/json",
        }

    def _post(self, payload: dict) -> requests.Response:

        try:
            resp = self._session.post(
                self._url(),
                headers=self._headers(),
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp
        except requests.exceptions.Timeout:
            print("[WhatsAppAdapter] Timeout al enviar mensaje")
            raise
        except requests.exceptions.RequestException as e:
            print(f"[WhatsAppAdapter] Error HTTP: {e}")
            raise

    # ─────────────────────────────────────────────────────────────────────────
    # MÉTODOS PÚBLICOS — cada uno representa un tipo de mensaje de WhatsApp
    # ─────────────────────────────────────────────────────────────────────────

    def enviar_texto(self, numero: str, mensaje: str) -> None:
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type":    "individual",
            "to":                numero,
            "type":              "text",
            "text": {
                "preview_url": False,
                "body":        mensaje,
            }
        }
        self._post(payload)

    def enviar_botones(
        self,
        numero:  str,
        cuerpo:  str,
        botones: list[dict]
    ) -> None:
      
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type":    "individual",
            "to":                numero,
            "type":              "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": cuerpo},
                "action": {
                    "buttons": [
                        {
                            "type":  "reply",
                            "reply": {"id": b["id"], "title": b["title"]}
                        }
                        for b in botones[:3]   # Meta permite máximo 3 botones
                    ]
                }
            }
        }
        self._post(payload)

    def enviar_lista(
        self,
        numero:      str,
        cuerpo:      str,
        boton_texto: str,
        secciones:   list[dict]
    ) -> None:
      
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type":    "individual",
            "to":                numero,
            "type":              "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": cuerpo},
                "action": {
                    "button":   boton_texto,
                    "sections": secciones,
                }
            }
        }
        self._post(payload)