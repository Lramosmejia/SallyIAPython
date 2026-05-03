from ..extensions import db


class Estudiante(db.Model):
    """Información académica de un estudiante."""

    __tablename__ = 'estudiantes'

    id                    = db.Column(db.Integer,     primary_key=True)
    numero_identificacion = db.Column(db.String(50),  unique=True, nullable=False)
    nombre                = db.Column(db.String(200), nullable=True)
    estado_academico      = db.Column(db.String(100), nullable=True)
    semestre              = db.Column(db.String(50),  nullable=True)
    horario               = db.Column(db.Text,        nullable=True)
    docentes              = db.Column(db.Text,        nullable=True)

    def __repr__(self) -> str:
        return f"<Estudiante #{self.id} [{self.numero_identificacion}] {self.nombre}>"

    def to_dict(self) -> dict:
        return {
            'id':                    self.id,
            'numero_identificacion': self.numero_identificacion,
            'nombre':                self.nombre,
            'estado_academico':      self.estado_academico,
            'semestre':              self.semestre,
            'horario':               self.horario,
            'docentes':              self.docentes,
        }