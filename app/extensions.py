from flask_sqlalchemy import SQLAlchemy
 
# Instancia única de SQLAlchemy — se inicializa con db.init_app(app) en la factory
db = SQLAlchemy()