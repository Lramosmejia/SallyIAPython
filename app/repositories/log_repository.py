from ..extensions import db
from ..models.log import Log


class LogRepository:
    """Gestiona el acceso a datos de la tabla logs."""

    def guardar(self, texto: str) -> Log:

        log = Log(texto=texto)
        db.session.add(log)
        db.session.commit()
        return log

    def listar_recientes(self, limite: int = 100) -> list[Log]:

        return (
            db.session.query(Log)
            .order_by(Log.fecha_y_hora.desc())
            .limit(limite)
            .all()
        )

    def contar(self) -> int:

        return db.session.query(Log).count()