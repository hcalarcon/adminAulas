from sqlalchemy.orm import Session
from src.modules.evaluacion.nota_model import NotaTarea
from src.modules.evaluacion.tarea_model import Tarea
from src.modules.usuarios.user_model import Usuarios
from src.modules.evaluacion.nota_schemas import (
    NotaTareaAsignacionMasiva,
    NotaTareaUpdate,
    NotaTareaCreate,
)
from fastapi import HTTPException


def asignar_tarea(db: Session, data: NotaTareaCreate):
    # Validar existencia de tarea y alumno
    tarea = db.query(Tarea).filter(Tarea.id == data.tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    alumno = db.query(Usuarios).filter(Usuarios.id == data.alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # Crear asignación
    asignacion = NotaTarea(**data.model_dump())
    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)
    return asignacion


def asignar_tarea_masiva(db: Session, data: NotaTareaAsignacionMasiva):
    # Validar que exista la tarea
    tarea = db.query(Tarea).filter(Tarea.id == data.tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    asignaciones = []
    for alumno_id in data.alumnos:
        alumno = db.query(Usuarios).filter(Usuarios.id == alumno_id).first()
        if not alumno:
            continue  # Opcional: podés lanzar error o solo omitir

        asignacion = NotaTarea(
            tarea_id=data.tarea_id,
            alumno_id=alumno_id,
            entregado=False,
            nota=None,
        )
        db.add(asignacion)
        asignaciones.append(asignacion)

    db.commit()
    for a in asignaciones:
        db.refresh(a)

    return asignaciones


def actualizar_nota_tarea(db: Session, nota_id: int, data: NotaTareaUpdate):
    nota = db.query(NotaTarea).filter(NotaTarea.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(nota, campo, valor)

    db.commit()
    db.refresh(nota)
    return nota


def eliminar_nota_tarea(db: Session, nota_id: int):
    nota = db.query(NotaTarea).filter(NotaTarea.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    db.delete(nota)
    db.commit()
    return {"msg": "Nota eliminada correctamente"}


def obtener_notas_por_alumno(db: Session, alumno_id: int):
    return db.query(NotaTarea).filter(NotaTarea.alumno_id == alumno_id).all()


def obtener_notas_por_tarea(db: Session, tarea_id: int):
    return db.query(NotaTarea).filter(NotaTarea.tarea_id == tarea_id).all()


def obtener_notas_por_alumno_y_aula(db: Session, alumno_id: int, aula_id: int):
    return (
        db.query(NotaTarea)
        .join(NotaTarea.tarea)
        .filter(NotaTarea.alumno_id == alumno_id, Tarea.aula_id == aula_id)
        .all()
    )
