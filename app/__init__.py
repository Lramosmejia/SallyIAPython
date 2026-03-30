from flask import Flask
from .extensions import db
from .config.settings import Config
 
 
def create_app(config_class=Config) -> Flask:
    """
    Factory que crea y configura la aplicación Flask.
 
    Ventajas:
    - Evita importaciones circulares
    - Permite crear instancias de testing fácilmente
    - Centraliza toda la inicialización
 
    Returns:
        Flask: Aplicación completamente configurada
    """
    app = Flask(
        __name__,
        template_folder='../templates'   # apunta a /templates en la raíz
    )
    app.config.from_object(config_class)
 
    # ── Inicializar extensiones ───────────────────────────────────────────────
    db.init_app(app)
 
    # ── Registrar Blueprints (Controllers) ───────────────────────────────────
    from .controllers.webhook_controller import webhook_bp
    app.register_blueprint(webhook_bp)
 
    # ── Crear tablas en la BD ─────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
 
    return app
