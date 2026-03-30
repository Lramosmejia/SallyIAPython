from flask import Blueprint, request, Response, render_template, current_app
from ..services.message_service import MessageService
from ..repositories.log_repository import LogRepository


webhook_bp = Blueprint('webhook', __name__)

# Instancias creadas una sola vez por proceso (patrón lazy singleton)
_service:    MessageService  | None = None
_repository: LogRepository   | None = None


def _get_service() -> MessageService:
    global _service
    if _service is None:
        _service = MessageService()
    return _service


def _get_repository() -> LogRepository:
    global _repository
    if _repository is None:
        _repository = LogRepository()
    return _repository


@webhook_bp.route('/')
def index():

    registros = _get_repository().listar_recientes(limite=100)
    return render_template('index.html', registros=registros)


@webhook_bp.route('/webhook', methods=['GET'])
def webhook_verify():

    mode      = request.args.get('hub.mode')
    token     = request.args.get('hub.verify_token', '').strip()
    challenge = request.args.get('hub.challenge', '')

    token_esperado = current_app.config.get('TOKEN_VERIFICACION', 'SALLY')

    if mode == 'subscribe' and token == token_esperado:
        print(f"[Webhook] Verificación exitosa ✅")
        return Response(challenge, status=200, mimetype='text/plain')

    print(f"[Webhook] Verificación FALLIDA ❌ — token recibido: '{token}'")
    return Response('Forbidden', status=403, mimetype='text/plain')


@webhook_bp.route('/webhook', methods=['POST'])
def webhook_receive():

    data = request.get_json(silent=True)

    if data:
        _get_service().procesar_webhook(data)

    # Meta requiere HTTP 200 con el texto exacto 'EVENT_RECEIVED'
    return Response('EVENT_RECEIVED', status=200, mimetype='text/plain')