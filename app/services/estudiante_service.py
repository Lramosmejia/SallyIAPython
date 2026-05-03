from ..repositories.estudiante_repository import EstudianteRepository
from ..models.estudiante_model import Estudiante


class EstudianteService:
    """Lógica de negocio para consulta y validación de estudiantes."""

    def __init__(self):
        self.repository = EstudianteRepository()

    def validar_estudiante(self, numero_identificacion: str) -> Estudiante | None:

        numero_limpio = numero_identificacion.replace('.', '').replace(' ', '').strip()

        return self.repository.obtener_estudiante_por_identificacion(numero_limpio)