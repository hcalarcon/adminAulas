from fastapi import APIRouter, Depends, Request, HTTPException
from src.schemas.alarcoins_schemas import (
    AlarcoinCreate,
    AulaAlarcoinOut,
    AlarcoinBase,
    AulaAlarcoinAlumnoOut,
)
from src.controllers import alarcoins_controller
from sqlalchemy.orm import Session
from src.api.deps import get_db
from typing import List

router = APIRouter()


@router.post("/")
def crear_alarcoin(
    request: Request, data: AlarcoinCreate, db: Session = Depends(get_db)
):
    if not request.state.user.is_teacher:
        raise HTTPException(
            status_code=403, detail="Solo los profesores pueden asignar alarcoins"
        )

    return alarcoins_controller.crear_alarcoin(db, data)


@router.put("/{id}")
def actualizar_alarcoin_endpoint(
    id: int, request: Request, data: AlarcoinBase, db: Session = Depends(get_db)
):
    if not request.state.user.is_teacher:
        raise HTTPException(
            status_code=403, detail="Solo los profesores pueden editar alarcoins"
        )

    return alarcoins_controller.actualizar_alarcoin(db, id, data)


@router.get("/me", response_model=List[AulaAlarcoinAlumnoOut])
def obtener_mis_alarcoin(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    return alarcoins_controller.obtener_alarcoins_por_alumno(db, user.id)


@router.get("/historial", response_model=List[AulaAlarcoinOut])
def historial_alarcoins_profesor(request: Request, db: Session = Depends(get_db)):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return alarcoins_controller.obtener_alarcoins_por_profesor(
        db, request.state.user.id
    )


# @router.get("/")
# def obtener_alarcoins_de_aula(
#     request: Request, data: AlumnoIdList, db: Session = Depends(get_db)
# ):
#     if not request.state.user.is_teacher:
#         raise HTTPException(
#             status_code=403,
#             detail="Solo los profesores pueden ver los alarcoins del aula",
#         )

#     return alarcoins_controller.obtener_alarcoins_por_aula(db, data.alumno_ids)
