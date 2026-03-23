from datetime import datetime, timezone
from flask import Flask, jsonify, request, render_template 
# importamos flask sqlalchemy para el manejo de la bd
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# confugiración de la base de datos SQLlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#modelo de una tabla para la base de datos
class Log (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    texto = db.Column(db.TEXT)

#create table
with app.app_context():
    db.create_all()
    
#orden de los registros por fecha y hora 
def orden_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.fecha_y_hora, reverse=True)

@app.route('/')
def index():
    #obtenemos los registros de la base de datos
    registros = Log.query.all()
    registros_ordenados = orden_por_fecha_y_hora(registros)
    return render_template('index.html', registros=registros_ordenados)

mensajes_log = []

# se define la función para guardar los mensajes en la base de datos
def agregar_mensajes_log(texto):
    mensajes_log.append(texto)
    
    #guardar mensajes en la base de datos 
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()
    
# token de verificacion para la configuracion 
TOKEN_SALLY = 'SALLY'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        challenge = verificar_token(request)
        return challenge
    elif request.method == 'POST':
        response = recibir_mensajes(request)
        return response
        
def verificar_token(req): 
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.verify_challenge')
    
    if challenge and token == TOKEN_SALLY:
        return challenge
    else:
        return jsonify ({'error' : 'token inválido'}), 401


def recibir_mensajes(req):
    req = request.get_json()
    agregar_mensajes_log(req)
    
    return jsonify({'message': 'EVENT_RECEIVED'})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)