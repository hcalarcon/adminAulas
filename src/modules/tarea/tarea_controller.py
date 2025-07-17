from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.modules.tarea.tarea_model import Tarea
from src.modules.nota.nota_model import NotaTarea
from src.modules.tarea.tarea_schemas import TareaCreate, TareaUpdate
from src.modules.aula.aulas_model import Aula, alumnos_aulas
from src.modules.usuarios.user_model import Usuarios
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


def listar_tareas_por_usuario(db: Session, user: Usuarios):
    # Si es profesor: tareas en sus aulas
    if user.is_teacher:
        # Aulas del profesor
        aulas = db.query(Aula).filter(Aula.profesor_id == user.id).all()
        tareas_data = []

        for aula in aulas:
            tareas = db.query(Tarea).filter(Tarea.aula_id == aula.id).all()

            for tarea in tareas:
                notas = tarea.notas
                entregados = sum(1 for nota in notas if nota.entregado)
                cantidad_alumnos = len(notas)

                tareas_data.append(
                    {
                        "id": tarea.id,
                        "titulo": tarea.titulo,
                        "descripcion": tarea.descripcion,
                        "tipo": tarea.tipo,
                        "fecha_creacion": tarea.fecha_creacion,
                        "fecha_limite": tarea.fecha_limite,
                        "aula_id": tarea.aula_id,
                        "created_by": tarea.created_by,
                        "cantidad_alumnos": cantidad_alumnos,
                        "entregados": entregados,
                    }
                )

        return tareas_data

    else:
        # Notas del alumno (solo sus tareas)
        notas = db.query(NotaTarea).filter(NotaTarea.alumno_id == user.id).all()
        tareas_data = []

        for nota in notas:
            tarea = nota.tarea
            tareas_data.append(
                {
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "tipo": tarea.tipo,
                    "fecha_creacion": tarea.fecha_creacion,
                    "fecha_limite": tarea.fecha_limite,
                    "aula_id": tarea.aula_id,
                    "created_by": tarea.created_by,
                    "entregado": nota.entregado,
                }
            )

        return tareas_data


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

    cantidad_alumnos = len(tarea.notas)
    entregados = sum(1 for nota in tarea.notas if nota.entregado)

    return {
        "id": tarea.id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "tipo": tarea.tipo,
        "fecha_creacion": tarea.fecha_creacion,
        "fecha_limite": tarea.fecha_limite,
        "aula_id": tarea.aula_id,
        "created_by": tarea.created_by,
        "cantidad_alumnos": cantidad_alumnos,
        "entregados": entregados,
    }


def eliminar_tarea(db: Session, tarea_id: int):
    tarea = obtener_tarea(db, tarea_id)
    db.delete(tarea)
    db.commit()
    return {"msg": "Tarea eliminada correctamente"}
