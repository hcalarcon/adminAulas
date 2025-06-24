from sqlalchemy.orm import Session, joinedload
from src.models.epetcoin_model import TransaccionCoin, EpetCoin
from src.schemas import epetcoins_schemas
from src.models.user_model import Usuarios
from src.models.aulas_model import Aula
from src.models.grupos_model import Grupos

# from src.schemas.epetcoins_schemas import AlarcoinCreate
from datetime import date
from fastapi import HTTPException


# def crear_alarcoin(db: Session, data: AlarcoinCreate):
#     nueva = Coin(
#         cantidad=data.cantidad,
#         detalle=data.detalle,
#         fecha=data.fecha or date.today(),
#         suma=data.suma if data.suma is not None else True,
#         alumno_id=data.alumno_id,
#         aula_id=data.aula_id,
#     )
#     db.add(nueva)
#     db.commit()
#     db.refresh(nueva)
#     return nueva


# def obtener_alarcoins_por_alumno(db: Session, alumno_id: int):
#     aulas = db.query(Aula).join(Aula.alumnos).filter(Usuarios.id == alumno_id).all()

#     resultado = []

#     for aula in aulas:
#         alarcoins = (
#             db.query(Coin)
#             .filter(Coin.alumno_id == alumno_id, Coin.aula_id == aula.id)
#             .all()
#         )

#         resultado.append(
#             {
#                 "aula_id": aula.id,
#                 "nombre": aula.nombre,
#                 "alarcoins": alarcoins,
#             }
#         )

#     return resultado


# def actualizar_alarcoin(db: Session, alarcoin_id: int, data: AlarcoinCreate):
#     alarcoin = db.query(Coin).filter(Coin.id == alarcoin_id).first()
#     if not alarcoin:
#         raise HTTPException(status_code=404, detail="Alarcoin no encontrado")

#     alarcoin.cantidad = data.cantidad
#     alarcoin.detalle = data.detalle
#     alarcoin.fecha = data.fecha or alarcoin.fecha
#     alarcoin.suma = data.suma if data.suma is not None else alarcoin.suma
#     alarcoin.aula_id = data.aula_id
#     alarcoin.alumno_id = data.alumno_id

#     db.commit()
#     db.refresh(alarcoin)
#     return alarcoin


# def obtener_alarcoins_por_aula(db: Session, aula_id: int):
#     return db.query(Coin).filter(Coin.aula_id == aula_id).all()


# def obtener_alarcoins_por_profesor(db: Session, profesor_id: int):
#     # Obtener las aulas del profesor
#     aulas = (
#         db.query(Aula)
#         .options(joinedload(Aula.alumnos).joinedload(Usuarios.coins_recibidos))
#         .filter(Aula.profesor_id == profesor_id)
#         .all()
#     )

#     resultado = []

#     for aula in aulas:
#         alumnos_con_alarcoins = []
#         for alumno in aula.alumnos:
#             # Filtrar solo los alarcoins de esa aula
#             alarcoins = [
#                 {
#                     "id": al.id,
#                     "cantidad": al.cantidad,
#                     "detalle": al.detalle,
#                     "fecha": al.fecha.isoformat(),
#                     "suma": al.suma,
#                 }
#                 for al in alumno.alarcoins
#                 if al.aula_id == aula.id
#             ]
#             alumnos_con_alarcoins.append(
#                 {
#                     "id": alumno.id,
#                     "alarcoins": alarcoins,
#                 }
#             )

#         resultado.append(
#             {
#                 "aula_id": aula.id,
#                 "nombre": aula.nombre,
#                 "alumnos": alumnos_con_alarcoins,
#             }
#         )


#     return resultado
def get_coin(db: Session, profesor_id: int):
    coin = db.query(EpetCoin).filter(EpetCoin.profesor_id == profesor_id).first()
    if coin:
        return coin
    return {"coin": False}


def crear_coin(db: Session, data: EpetCoin, profesor_id: int):
    # Verificar si ya tiene una moneda activa
    existente = db.query(EpetCoin).filter(EpetCoin.profesor_id == profesor_id).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya tienes una moneda activa")

    nueva_moneda = EpetCoin(
        nombre=data.nombre,
        profesor_id=profesor_id,
    )
    db.add(nueva_moneda)
    db.commit()
    db.refresh(nueva_moneda)
    return nueva_moneda


def crear_transaccion(
    db: Session, data: epetcoins_schemas.TransaccionCoinBase, profesor_id: int
):

    moneda = db.query(EpetCoin).filter(EpetCoin.profesor_id == profesor_id).first()
    if not moneda:
        raise HTTPException(
            status_code=200, detail="El profesor no tiene moneda activa"
        )
    suma = False
    if data.suma == 1:
        suma = True
    else:
        suma = False

    transaccion = TransaccionCoin(
        cantidad=data.cantidad,
        detalle=data.detalle,
        fecha=date.today(),
        suma=suma,
        alumno_id=data.alumno_id,
        moneda_id=moneda.id,
        aula_id=data.aula_id,
    )
    db.add(transaccion)
    db.commit()
    db.refresh(transaccion)
    return transaccion


def obtener_transaccioncoins_por_alumno(db: Session, alumno_id: int):
    transacciones = (
        db.query(TransaccionCoin)
        .join(EpetCoin)
        .filter(TransaccionCoin.alumno_id == alumno_id)
        .all()
    )

    resultado = {}
    for t in transacciones:
        aula_id = t.aula_id
        if aula_id not in resultado:
            resultado[aula_id] = {
                "aula_id": aula_id,
                "nombre_moneda": t.moneda.nombre,
                "epetcoins": [],
            }
        resultado[aula_id]["epetcoins"].append(
            {
                "id": t.id,
                "cantidad": t.cantidad,
                "detalle": t.detalle,
                "fecha": t.fecha.isoformat(),
                "suma": t.suma,
            }
        )

    return list(resultado.values())


def obtener_epetcoin_de_profesor(db: Session, profesor_id: int):
    moneda = db.query(EpetCoin).filter(EpetCoin.profesor_id == profesor_id).first()
    if not moneda:
        raise HTTPException(status_code=404, detail="No tienes una moneda activa")

    # Obtener transacciones de esa moneda
    transacciones = (
        db.query(TransaccionCoin)
        .options(joinedload(TransaccionCoin.aula), joinedload(TransaccionCoin.alumno))
        .filter(TransaccionCoin.moneda_id == moneda.id)
        .all()
    )

    # Agrupar transacciones por (alumno, aula)
    trans_por_alumno_aula: dict[tuple[int, int], list] = {}

    for t in transacciones:
        key = (t.alumno_id, t.aula_id)
        if key not in trans_por_alumno_aula:
            trans_por_alumno_aula[key] = []
        trans_por_alumno_aula[key].append(
            {
                "id": t.id,
                "cantidad": t.cantidad,
                "detalle": t.detalle,
                "fecha": t.fecha.isoformat(),
                "suma": t.suma,
            }
        )

    resultado = []

    # AULAS COMUNES
    aulas_comunes = (
        db.query(Aula)
        .options(joinedload(Aula.alumnos))
        .filter(Aula.profesor_id == profesor_id, Aula.tipo != "taller")
        .all()
    )

    for aula in aulas_comunes:
        alumnos_data = []
        for alumno in aula.alumnos:
            key = (alumno.id, aula.id)
            alumnos_data.append(
                {"id": alumno.id, "epetcoins": trans_por_alumno_aula.get(key, [])}
            )

        resultado.append(
            {"aula_id": aula.id, "nombre": aula.nombre, "alumnos": alumnos_data}
        )

    # AULAS TIPO TALLER (mediante grupos)
    aulas_taller = (
        db.query(Aula)
        .options(joinedload(Aula.grupos).joinedload(Grupos.alumnos))
        .filter(Aula.profesor_id == profesor_id, Aula.tipo == "taller")
        .all()
    )

    for aula in aulas_taller:
        alumnos_map: dict[int, dict] = {}

        for grupo in aula.grupos:
            for alumno in grupo.alumnos:
                if alumno.id not in alumnos_map:
                    key = (alumno.id, aula.id)
                    alumnos_map[alumno.id] = {
                        "id": alumno.id,
                        "epetcoins": trans_por_alumno_aula.get(key, []),
                    }

        resultado.append(
            {
                "aula_id": aula.id,
                "nombre": aula.nombre,
                "alumnos": list(alumnos_map.values()),
            }
        )

    return resultado
