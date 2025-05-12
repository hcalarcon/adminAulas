from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.clase_model import Clase
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
    return db.query(Clase).filter(Clase.aula_id == aula_id).all()


# validad el aula


def crear_clases_masivas(db: Session, aula_id: int, clases_data: List[dict]):
    # aula = db.query(Aula).filter(Aula.id == aula_id).first() validad aula
    # if not aula:
    #   raise HTTPException(status_code=404, detail="Aula no encontrada")

    nuevas_clases = []
    for clase in clases_data:
        nueva_clase = Clase(aula_id=aula_id, tema=clase["tema"], fecha=clase["fecha"])
        db.add(nueva_clase)
        nuevas_clases.append(nueva_clase)

    db.commit()
    return nuevas_clases
