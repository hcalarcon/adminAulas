from sqlalchemy.orm import Session
from src.models.aulasModel import Aula
from src.schemas import aulaSchemas
from fastapi import HTTPException
from src.utility.exist import existe


def get_aula(db: Session):
    return db.query(Aula).all()


def crear_aula(db: Session, aula: aulaSchemas.AulaCreate):
    nueva_aula = Aula(
        nombre=aula.nombre,
        ano=aula.ano,
        division=aula.division,
        especialidad=aula.especialidad,
    )
    db.add(nueva_aula)
    db.commit()
    db.refresh(nueva_aula)
    return nueva_aula


def get_aula_by_id(db: Session, id: int):
    # db_aula = db.query(Aula).filter(Aula.id == id).first()
    db_aula = existe(db, Aula, id=id)
    if not db_aula:
        raise HTTPException(status_code=401, detail="El aula no existe")

    return db_aula


def update_aula(db: Session, aula: aulaSchemas.AulaUpdate, id: int):
    db_aula = get_aula_by_id(db, id)

    if aula.nombre is not None:
        db_aula.nombre = aula.nombre
    if aula.ano is not None:
        db_aula.ano = aula.ano
    if aula.division is not None:
        db_aula.division = aula.division
    if aula.especialidad is not None:
        db_aula.especialidad = aula.especialidad

    db.commit()
    db.refresh(db_aula)
    return db_aula


def delete_aula(db: Session, id: int):

    db_aula = db.query(Aula).filter(Aula.id == id).first()

    db.delete(db_aula)
    db.commit()
    return db_aula
