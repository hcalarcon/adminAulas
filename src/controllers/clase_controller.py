from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.clase_model import Clase
from src.models.user_model import Usuarios
from src.schemas.clases_schemas import ClaseCreate, ClaseUpdate
from typing import List


def crear_clase(db: Session, clase_data: ClaseCreate):
    clase = Clase(
        fecha=clase_data.fecha, tema=clase_data.tema, aula_id=clase_data.aula_id
    )
    db.add(clase)
    db.commit()
    db.refresh(clase)
    return clase


def actualizar_clase(db: Session, clase_id: int, clase_data: ClaseUpdate):
    clase = db.query(Clase).filter(Clase.id == clase_id).first()
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    for field, value in clase_data.model_dump(exclude_unset=True).items():
        setattr(clase, field, value)

    db.commit()
    db.refresh(clase)
    return clase


def eliminar_clase(db: Session, clase_id: int):
    clase = db.query(Clase).filter(Clase.id == clase_id).first()
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    db.delete(clase)
    db.commit()
    return clase


def obtener_clase(db: Session, clase_id: int):
    clase = db.query(Clase).filter(Clase.id == clase_id).first()
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    return clase


def obtener_clases_por_aula(db: Session, aula_id: int):
    return db.query(Clase).filter(Clase.aula_id == aula_id).order_by(Clase.fecha).all()


def obtener_clases_para_alumno(db: Session, alumno_id: int, aula_id: int):
    print(alumno_id)
    alumno = db.query(Usuarios).filter(Usuarios.id == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    grupo_id = alumno.grupo_id

    # Verificamos que el alumno esté inscripto en el aula
    # if aula_id not in [a.id for a in alumno.aulas_inscripto]:
    #     raise HTTPException(status_code=403, detail="No estás inscripto en esta aula")

    clases = (
        db.query(Clase)
        .filter(
            Clase.aula_id == aula_id,
            (
                (Clase.grupo_id == None) | (Clase.grupo_id == grupo_id)
            ),  # teoría o grupo propio
        )
        .order_by(Clase.fecha)
        .all()
    )

    return clases


# validad el aula


def crear_clases_masivas(db: Session, aula_id: int, clases_data: List[dict]):
    nuevas_clases = []
    for clase in clases_data:
        nueva_clase = Clase(
            aula_id=aula_id,
            tema=clase["tema"],
            fecha=clase["fecha"],
            grupo_id=clase.get("grupo_id"),  # puede ser None (materia teoría)
            cuatrimestre=clase["cuatrimestre"],
        )
        db.add(nueva_clase)
        nuevas_clases.append(nueva_clase)

    db.commit()
    return nuevas_clases
