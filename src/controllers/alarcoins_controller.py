from sqlalchemy.orm import Session
from models import Alarcoin
from src.schemas.alarcoins_schemas import AlarcoinCreate
from datetime import date


def crear_alarcoin(db: Session, data: AlarcoinCreate):
    nueva = Alarcoin(
        cantidad=data.cantidad,
        detalle=data.detalle,
        fecha=data.fecha or date.today(),
        alumno_id=data.alumno_id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def obtener_alarcoins_por_alumno(db: Session, alumno_id: int):
    return db.query(Alarcoin).filter(Alarcoin.alumno_id == alumno_id).all()
