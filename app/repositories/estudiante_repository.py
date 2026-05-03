from ..models.estudiante_model import Estudiante
from ..extensions import db


class EstudianteRepository:
    """Gestiona el acceso a datos de la tabla estudiantes."""

    def obtener_estudiante_por_identificacion(self, numero_identificacion: str) -> Estudiante | None:

        return (
            db.session.query(Estudiante)
            .filter_by(numero_identificacion=numero_identificacion)
            .first()
        )