from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.grupos_model import Grupos
from src.models.user_model import Usuarios
from src.schemas import grupos_schemas
from src.models.aulas_model import Aula


def crear_grupo(db: Session, datos: grupos_schemas.GrupoCreate):
    grupo = Grupos(**datos.dict())
    db.add(grupo)
    db.commit()
    db.refresh(grupo)
    return grupo


def listar_grupos(db: Session, aula_id: int = None):
    query = db.query(Grupos)
    if aula_id:
        query = query.filter(Grupos.aula_id == aula_id)
    return query.all()


def actualizar_grupos(db: Session, updates: list[grupos_schemas.GrupoUpdate]):
    actualizados = []
    for grupo_data in updates:
        grupo = db.query(Grupos).get(grupo_data.id)
        if not grupo:
            continue
        for key, value in grupo_data.dict(exclude_unset=True).items():
            setattr(grupo, key, value)
        db.commit()
        db.refresh(grupo)
        actualizados.append(grupo)
    return actualizados


def eliminar_grupos(db: Session, grupo_ids: list[int]):
    db.query(Grupos).filter(Grupos.id.in_(grupo_ids)).delete(synchronize_session=False)
    db.commit()


def asignar_alumnos(db: Session, data: grupos_schemas.AsignarAlumnosSchema):
    grupo = db.query(Grupos).get(data.grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    for alumno_id in data.alumnos_ids:
        alumno = db.query(Usuarios).get(alumno_id)
        if not alumno:
            continue
        grupo.alumnos.append(alumno)

    db.commit()
    return grupo


def eliminar_alumnos_de_grupo(db: Session, data: grupos_schemas.EliminarAlumnosSchema):
    grupo = db.query(Grupos).get(data.grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    grupo.alumnos = [a for a in grupo.alumnos if a.id not in data.alumnos_ids]
    db.commit()
    return grupo


def asignar_aula_a_grupo(db: Session, grupo_id: int, aula_id: int):
    grupo = db.query(Grupos).get(grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    aula = db.query(Aula).get(aula_id)
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    grupo.aulas.append(aula)
    db.commit()
    db.refresh(grupo)
    return grupo
