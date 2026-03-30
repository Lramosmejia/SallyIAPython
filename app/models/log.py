from datetime import datetime, timezone
from ..extensions import db
 
class Log(db.Model):
    """Registro de un mensaje recibido o evento del chatbot."""

    __tablename__ = 'logs'

    id           = db.Column(db.Integer,  primary_key=True)
    fecha_y_hora = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    texto        = db.Column(db.TEXT, nullable=False)

    def __repr__(self) -> str:
        preview = self.texto[:40] if self.texto else ''
        return f"<Log #{self.id} [{self.fecha_y_hora}]: {preview}>"

    def to_dict(self) -> dict:
        
        return {
            'id':           self.id,
            'fecha_y_hora': self.fecha_y_hora.isoformat() if self.fecha_y_hora else None,
            'texto':        self.texto,
        }