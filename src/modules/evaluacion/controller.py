from sqlalchemy.orm import Session
from src.modules.evaluacion.model import CriterioEvaluacion
from src.modules.evaluacion.schemas import (
    CriterioEvaluacionCreate,
    CriterioEvaluacionUpdate,
)
from fastapi import HTTPException
from decimal import Decimal


def validar_suma_criterios(
    db: Session, aula_id: int, nuevo_peso: Decimal, excluir_id: int = None
):
    query = db.query(CriterioEvaluacion).filter(CriterioEvaluacion.aula_id == aula_id)
    if excluir_id:
        query = query.filter(CriterioEvaluacion.id != excluir_id)
    suma = sum([c.peso for c in query.all()])
    if suma + nuevo_peso > 100:
        raise HTTPException(status_code=400, detail="La suma de los pesos supera 100%")


def crear_criterio(db: Session, data: CriterioEvaluacionCreate):
    validar_suma_criterios(db, data.aula_id, data.peso)
    criterio = CriterioEvaluacion(**data.model_dump())
    db.add(criterio)
    db.commit()
    db.refresh(criterio)
    return criterio


def actualizar_criterio(db: Session, criterio_id: int, data: CriterioEvaluacionUpdate):
    criterio = (
        db.query(CriterioEvaluacion)
        .filter(CriterioEvaluacion.id == criterio_id)
        .first()
    )
    if not criterio:
        raise HTTPException(status_code=404, detail="Criterio no encontrado")
    validar_suma_criterios(db, criterio.aula_id, data.peso, excluir_id=criterio_id)
    for k, v in data.model_dump().items():
        setattr(criterio, k, v)
    db.commit()
    db.refresh(criterio)
    return criterio


def eliminar_criterio(db: Session, criterio_id: int):
    criterio = (
        db.query(CriterioEvaluacion)
        .filter(CriterioEvaluacion.id == criterio_id)
        .first()
    )
    if not criterio:
        raise HTTPException(status_code=404, detail="Criterio no encontrado")
    db.delete(criterio)
    db.commit()
    return {"msg": "Criterio eliminado correctamente"}


def listar_criterios(db: Session, aula_id: int):
    return (
        db.query(CriterioEvaluacion).filter(CriterioEvaluacion.aula_id == aula_id).all()
    )
