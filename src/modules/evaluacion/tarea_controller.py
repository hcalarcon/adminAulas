from sqlalchemy.orm import Session
from src.modules.evaluacion.tarea_model import Tarea
from src.modules.evaluacion.tarea_schemas import TareaCreate, TareaUpdate
from fastapi import HTTPException
from src.utility.fecha import get_today


def crear_tarea(db: Session, tarea: TareaCreate):
    nueva = Tarea(**tarea.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def listar_tareas_por_aula(db: Session, aula_id: int):
    return db.query(Tarea).filter(Tarea.aula_id == aula_id).all()


def obtener_tarea(db: Session, tarea_id: int):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


def actualizar_tarea(db: Session, tarea_id: int, data: TareaUpdate):
    tarea = obtener_tarea(db, tarea_id)
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(tarea, campo, valor)
    db.commit()
    db.refresh(tarea)
    return tarea


def eliminar_tarea(db: Session, tarea_id: int):
    tarea = obtener_tarea(db, tarea_id)
    db.delete(tarea)
    db.commit()
    return {"msg": "Tarea eliminada correctamente"}
