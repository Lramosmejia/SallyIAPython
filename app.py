from datetime import datetime, timezone
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
import requests 
import os

app = Flask(__name__)

# =========================
# CONFIGURACIÓN BASE DE DATOS
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# MODELO
# =========================
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    texto = db.Column(db.TEXT)

with app.app_context():
    db.create_all()

# =========================
# FUNCIONES AUXILIARES
# =========================
def orden_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.fecha_y_hora, reverse=True)


def agregar_mensajes_log(texto):
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()


# =========================
# CONFIGURACIÓN TOKEN
# =========================
TOKEN_SALLY = 'SALLY'


# =========================
# RUTA PRINCIPAL
# =========================
@app.route('/')
def index():
    registros = Log.query.all()
    registros_ordenados = orden_por_fecha_y_hora(registros)
    return render_template('index.html', registros=registros_ordenados)


# =========================
# WEBHOOK
# =========================
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():

    # VERIFICACIÓN META
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token and token.strip() == TOKEN_SALLY:
            return Response(challenge, status=200, mimetype='text/plain')
        else:
            return Response('Forbidden', status=403, mimetype='text/plain')

    # RECEPCIÓN DE MENSAJES
    elif request.method == 'POST':
        data = request.get_json()

        try:
            mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            numero = data['entry'][0]['changes'][0]['value']['messages'][0]['from']

            agregar_mensajes_log(f"{numero}: {mensaje}")

            #  RESPUESTA AUTOMÁTICA
            enviar_mensajes_whatsapp(numero, mensaje)

        except Exception as e:
            print("Error procesando mensaje:", e)

        return Response('EVENT_RECEIVED', status=200)


# =========================
# FUNCIÓN ENVIAR MENSAJES
# =========================
def enviar_mensajes_whatsapp(numero, mensaje_recibido):

    # 🔹 Lógica de respuesta
    if "hola" in mensaje_recibido.lower():
        respuesta = "¡Hola! mi nombre es Sally, soy tu chatbot universitario, ¿en qué puedo ayudarte?"
    else:
        respuesta = "No entendí tu mensaje, pero puedo ayudarte"

    # CONFIGURACIÓN (puedes ocultar luego)
    ACCESS_TOKEN = "EAAfOFtLFLgABRH7YgDg23z5nTusGt0AGLOfyRu0bsr4cNWDAky05ZBN71pAmgwKyDmlIpaXW8EofKV2pZC8AaZASuZCBrOWRsWD3m50a0JQLuKqZCmZBh3qtpSI6hzs34YfZAW4ZBVnmneOckVGxDfrGIu0KeMQl16YAF4ZCIeBYzZBs55vO2Dk79tFqLYzXA25ezG9jsfKoJg08xDxWzZBLaGH4BchRIoqCXi8JiHaqKFgvo6BxEBdXbztCH38LnfvwlhbHTFxEFOkNHURsnSOQPg9mZCaaeQZDZD"
    PHONE_NUMBER_ID = "997842246750668"

    
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": respuesta
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        print("Respuesta Meta:", response.status_code, response.text)

    except Exception as e:
        print("Error enviando mensaje:", e)


# =========================
# CONFIGURACIÓN RENDER
# =========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
