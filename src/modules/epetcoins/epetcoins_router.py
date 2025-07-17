from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.api.deps import get_db
from src.modules.epetcoins import epetcoins_controller
from src.modules.epetcoins.epetcoins_schemas import (
    EpetCoinBase,
    TransaccionCoinOut,
    TransaccionCoinBase,
    EpetCoinOut,
)

router = APIRouter()


@router.post("/moneda", response_model=EpetCoinOut)
def activar_mi_moneda(request: Request, nombre: str, db: Session = Depends(get_db)):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(
            status_code=403, detail="Solo los profesores pueden crear su coin"
        )

    return epetcoins_controller.crear_epetcoin(db, nombre=nombre, profesor_id=user.id)


@router.post("/", response_model=EpetCoinBase)
def asignar_coin(request: Request, data: EpetCoinOut, db: Session = Depends(get_db)):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(
            status_code=403, detail="Solo los profesores pueden asignar coins"
        )

    return epetcoins_controller.crear_coin(db, data, profesor_id=user.id)


@router.post("/transaccion", response_model=TransaccionCoinOut)
def asignar_coin(
    request: Request, data: TransaccionCoinBase, db: Session = Depends(get_db)
):
    print(data)
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(
            status_code=403, detail="Solo los profesores pueden asignar coins"
        )

    return epetcoins_controller.crear_transaccion(db, data, profesor_id=user.id)


@router.get(
    "/historial",
)
def historial_de_mis_coins(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    if user.is_teacher:
        return epetcoins_controller.obtener_epetcoin_de_profesor(
            db, profesor_id=user.id
        )
    return epetcoins_controller.obtener_transaccioncoins_por_alumno(db, user.id)


#  response_model=List[AulaCoinAlumnoOut]
# obtener la moneda del profesor
@router.get("/me")
def mis_coins(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    if user.is_teacher:
        return epetcoins_controller.get_coin(db, profesor_id=user.id)
