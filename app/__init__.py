from flask import Flask
from .extensions import db
from .config.settings import Config
from .controllers.webhook_controller import webhook_bp
from .seeds import seed_estudiantes

def create_app(config_class=Config) -> Flask:

    app = Flask(
        __name__,
         # apunta a /templates en la raíz
        template_folder='../templates'  
    )
    app.config.from_object(config_class)

    # ── Inicializar extensiones 
    db.init_app(app)

    # ── Registrar Blueprints (Controllers) 
    app.register_blueprint(webhook_bp)

    # ── Crear tablas en la BD 
    with app.app_context():
        db.create_all()
        print("base de datos creada con exito")
        seed_estudiantes()
    return app