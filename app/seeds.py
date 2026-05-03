from .extensions import db
from .models.estudiante_model import Estudiante

ESTUDIANTES_PRUEBA = [
    {
        'numero_identificacion': '1001',
        'nombre':                'Juan Perez',
        'estado_academico':      'ACTIVO',
        'semestre':              '5',
        'horario':               'Mañana',
        'docentes':              'Lopez, Martinez',
    },
    {
        'numero_identificacion': '1002',
        'nombre':                'Maria Gomez',
        'estado_academico':      'SUSPENDIDO',
        'semestre':              '3',
        'horario':               'Tarde',
        'docentes':              'Ruiz',
    },
    {
        'numero_identificacion': '1003',
        'nombre':                'Carlos Diaz',
        'estado_academico':      'ACTIVO',
        'semestre':              '8',
        'horario':               'Nocturno',
        'docentes':              'Torres',
    },
]


def seed_estudiantes() -> None:
    """Inserta los estudiantes de prueba si aún no existen en la BD."""

    insertados = 0

    for datos in ESTUDIANTES_PRUEBA:
        existe = (
            db.session.query(Estudiante)
            .filter_by(numero_identificacion=datos['numero_identificacion'])
            .first()
        )
        if not existe:
            db.session.add(Estudiante(**datos))
            insertados += 1

    if insertados:
        db.session.commit()
        print(f"[Seed] {insertados} estudiante(s) de prueba insertado(s).")
    else:
        print("[Seed] Estudiantes de prueba ya existen. No se insertó nada.")