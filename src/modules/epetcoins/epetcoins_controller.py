from sqlalchemy.orm import Session, joinedload
from src.modules.epetcoins.epetcoin_model import TransaccionCoin, EpetCoin
from src.modules.epetcoins import epetcoins_schemas
from src.modules.usuarios.user_model import Usuarios
from src.modules.aula.aulas_model import Aula
from src.modules.grupos.grupos_model import Grupos
from src.utility.fecha import get_today
from fastapi import HTTPException


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
        fecha=get_today(),
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
