from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.schemas import clases_schemas
from src.controllers import clase_controller
from typing import List
from src.core.limiter import limiter  # Asegurate de importar bien el limiter

router = APIRouter()


@router.post("/masivas", response_model=List[clases_schemas.ClaseOut])
@limiter.limit("10/minute")
def crear_clases_masivas(
    request_data: clases_schemas.ClasesMasivasRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return clase_controller.crear_clases_masivas(
        db, request_data.aula_id, [clase.model_dump() for clase in request_data.clases]
    )


@router.get("/aulas/{aula_id}/clases", response_model=List[clases_schemas.ClaseOut])
@limiter.limit("30/minute")
def get_clases_por_aula(aula_id: int, request: Request, db: Session = Depends(get_db)):

    return clase_controller.obtener_clases_por_aula(db, aula_id)


@router.post("/", response_model=clases_schemas.ClaseOut)
@limiter.limit("10/minute")
def crear_clase(
    clase: clases_schemas.ClaseCreate, request: Request, db: Session = Depends(get_db)
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return clase_controller.crear_clase(db, clase)


@router.put("/{id}", response_model=clases_schemas.ClaseOut)
@limiter.limit("10/minute")
def actualizar_clase(
    id: int,
    clase: clases_schemas.ClaseUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return clase_controller.actualizar_clase(db, id, clase)


@router.delete("/{id}", response_model=clases_schemas.ClaseOut)
@limiter.limit("10/minute")
def eliminar_clase(id: int, request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return clase_controller.eliminar_clase(db, id)


@router.get("/{id}", response_model=clases_schemas.ClaseOut)
@limiter.limit("30/minute")
def obtener_clase(id: int, request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return clase_controller.obtener_clase(db, id)
