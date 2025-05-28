from sqlalchemy.orm import Session, joinedload
from src.models.alarcoins_model import Alarcoin
from src.models.user_model import Usuarios
from src.models.aulas_model import Aula


from src.schemas.alarcoins_schemas import AlarcoinCreate
from datetime import date
from fastapi import HTTPException


def crear_alarcoin(db: Session, data: AlarcoinCreate):
    nueva = Alarcoin(
        cantidad=data.cantidad,
        detalle=data.detalle,
        fecha=data.fecha or date.today(),
        suma=data.suma if data.suma is not None else True,
        alumno_id=data.alumno_id,
        aula_id=data.aula_id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def obtener_alarcoins_por_alumno(db: Session, alumno_id: int):
    aulas = db.query(Aula).join(Aula.alumnos).filter(Usuarios.id == alumno_id).all()

    resultado = []

    for aula in aulas:
        alarcoins = (
            db.query(Alarcoin)
            .filter(Alarcoin.alumno_id == alumno_id, Alarcoin.aula_id == aula.id)
            .all()
        )

        resultado.append(
            {
                "aula_id": aula.id,
                "nombre": aula.nombre,
                "alarcoins": alarcoins,
            }
        )

    return resultado


def actualizar_alarcoin(db: Session, alarcoin_id: int, data: AlarcoinCreate):
    alarcoin = db.query(Alarcoin).filter(Alarcoin.id == alarcoin_id).first()
    if not alarcoin:
        raise HTTPException(status_code=404, detail="Alarcoin no encontrado")

    alarcoin.cantidad = data.cantidad
    alarcoin.detalle = data.detalle
    alarcoin.fecha = data.fecha or alarcoin.fecha
    alarcoin.suma = data.suma if data.suma is not None else alarcoin.suma
    alarcoin.aula_id = data.aula_id
    alarcoin.alumno_id = data.alumno_id

    db.commit()
    db.refresh(alarcoin)
    return alarcoin


def obtener_alarcoins_por_aula(db: Session, aula_id: int):
    return db.query(Alarcoin).filter(Alarcoin.aula_id == aula_id).all()


def obtener_alarcoins_por_profesor(db: Session, profesor_id: int):
    # Obtener las aulas del profesor
    aulas = (
        db.query(Aula)
        .options(joinedload(Aula.alumnos).joinedload(Usuarios.alarcoins))
        .filter(Aula.profesor_id == profesor_id)
        .all()
    )

    resultado = []

    for aula in aulas:
        alumnos_con_alarcoins = []
        for alumno in aula.alumnos:
            # Filtrar solo los alarcoins de esa aula
            alarcoins = [
                {
                    "id": al.id,
                    "cantidad": al.cantidad,
                    "detalle": al.detalle,
                    "fecha": al.fecha.isoformat(),
                    "suma": al.suma,
                }
                for al in alumno.alarcoins
                if al.aula_id == aula.id
            ]
            alumnos_con_alarcoins.append(
                {
                    "id": alumno.id,
                    "alarcoins": alarcoins,
                }
            )

        resultado.append(
            {
                "aula_id": aula.id,
                "nombre": aula.nombre,
                "alumnos": alumnos_con_alarcoins,
            }
        )

    return resultado
