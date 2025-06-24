from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.api.deps import get_db
from src.controllers import epetcoins_controller
from src.schemas.epetcoins_schemas import (
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


# @router.get("/moneda/me", response_model=EpetCoinOut)
# def obtener_mi_epetcoin(request: Request, db: Session = Depends(get_db)):
#     user = request.state.user
#     return epetcoins_controller.obtener_epetcoin_de_profesor(db, profesor_id=user.id)


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
    # return epetcoins_controller.obtener_coins_por_alumno(db, alumno_id=user.id)


# from fastapi import APIRouter, Depends, Request, HTTPException
# from src.schemas.epetcoins_schemas import (
#     AlarcoinCreate,
#     AulaAlarcoinOut,
#     AlarcoinBase,
#     AulaAlarcoinAlumnoOut,
# )
# from src.controllers import epetcoins_controller
# from sqlalchemy.orm import Session
# from src.api.deps import get_db
# from typing import List

# router = APIRouter()


# @router.post("/")
# def crear_alarcoin(
#     request: Request, data: AlarcoinCreate, db: Session = Depends(get_db)
# ):
#     if not request.state.user.is_teacher:
#         raise HTTPException(
#             status_code=403, detail="Solo los profesores pueden asignar alarcoins"
#         )

#     return epetcoins_controller.crear_alarcoin(db, data)


# @router.put("/{id}")
# def actualizar_alarcoin_endpoint(
#     id: int, request: Request, data: AlarcoinBase, db: Session = Depends(get_db)
# ):
#     if not request.state.user.is_teacher:
#         raise HTTPException(
#             status_code=403, detail="Solo los profesores pueden editar alarcoins"
#         )

#     return epetcoins_controller.actualizar_alarcoin(db, id, data)


# @router.get("/me", response_model=List[AulaAlarcoinAlumnoOut])
# def obtener_mis_alarcoin(request: Request, db: Session = Depends(get_db)):
#     user = request.state.user
#     return epetcoins_controller.obtener_alarcoins_por_alumno(db, user.id)


# @router.get("/historial", response_model=List[AulaAlarcoinOut])
# def historial_alarcoins_profesor(request: Request, db: Session = Depends(get_db)):
#     if not request.state.user.is_teacher:
#         raise HTTPException(status_code=403, detail="No autorizado")
#     return epetcoins_controller.obtener_alarcoins_por_profesor(
#         db, request.state.user.id
#     )


# # @router.get("/")
# # def obtener_alarcoins_de_aula(
# #     request: Request, data: AlumnoIdList, db: Session = Depends(get_db)
# # ):
# #     if not request.state.user.is_teacher:
# #         raise HTTPException(
# #             status_code=403,
# #             detail="Solo los profesores pueden ver los alarcoins del aula",
# #         )

# #     return alarcoins_controller.obtener_alarcoins_por_aula(db, data.alumno_ids)
