from datetime import datetime, timezone
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    texto = db.Column(db.TEXT)

with app.app_context():
    db.create_all()

# Ordenar registros
def orden_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.fecha_y_hora, reverse=True)

@app.route('/')
def index():
    registros = Log.query.all()
    registros_ordenados = orden_por_fecha_y_hora(registros)
    return render_template('index.html', registros=registros_ordenados)

# Token
TOKEN_SALLY = 'SALLY'


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.verify_challenge')

        
        if token and token.strip() == TOKEN_SALLY:
            return challenge, 200
        else:
            return 'Token inválido', 403

    elif request.method == 'POST':
        data = request.get_json()

        
        agregar_mensajes_log(str(data))

        return 'EVENT_RECEIVED', 200

# Guardar mensajes
def agregar_mensajes_log(texto):
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port)
