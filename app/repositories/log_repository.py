from ..extensions import db
from ..models.log import Log


class LogRepository:
    """Gestiona el acceso a datos de la tabla logs."""

    def guardar(self, texto: str) -> Log:
        """
        Persiste un nuevo log en la base de datos.

        Args:
            texto: Mensaje a registrar (ej: "573001234567: hola")

        Returns:
            Log: El objeto guardado con su ID asignado
        """
        log = Log(texto=texto)
        db.session.add(log)
        db.session.commit()
        return log

    def listar_recientes(self, limite: int = 100) -> list[Log]:
        """
        Obtiene los logs más recientes, ordenados de nuevo a viejo.

        Usa ORDER BY en la consulta (más eficiente que sorted() en Python,
        que era el patrón del código original).

        Args:
            limite: Máximo de registros a devolver (default: 100)

        Returns:
            list[Log]: Lista de logs ordenados por fecha descendente
        """
        return (
            db.session.query(Log)
            .order_by(Log.fecha_y_hora.desc())
            .limit(limite)
            .all()
        )

    def contar(self) -> int:
        """Devuelve el total de logs almacenados."""
        return db.session.query(Log).count()