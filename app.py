from datetime import datetime, timezone
from flask import Flask, render_template 
# importamos flask sqlalchemy para el manejo de la bd
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# confugiración de la base de datos SQLlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#modelo de una tabla para la base de datos
class Log (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime,default = datetime.now(timezone.utc))
    texto = db.Column(db.TEXT)

#create table
with app.app_context():
    db.create_all()
    
    prueba1 = Log(texto = "mensaje de prueba 1")
    prueba2 = Log(texto = "mensaje de prueba 2")
    
    db.session.add(prueba1)
    db.session.add(prueba2)
    db.session.commit()

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
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True) 