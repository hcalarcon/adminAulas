from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.core.limiter import limiter
from src.modules.evaluacion.schemas import (
    CriterioEvaluacionCreate,
    CriterioEvaluacionOut,
    CriterioEvaluacionUpdate,
)
from src.modules.evaluacion import controller as evaluacion_controller
from typing import List

router = APIRouter()


@router.post("/", response_model=CriterioEvaluacionOut)
@limiter.limit("10/minute")
def crear(
    request: Request, data: CriterioEvaluacionCreate, db: Session = Depends(get_db)
):
    if not request.state.user.is_teacher:
        raise HTTPException(
            status_code=403, detail="Solo profesores pueden crear criterios"
        )
    return evaluacion_controller.crear_criterio(db, data)


@router.put("/{criterio_id}", response_model=CriterioEvaluacionOut)
@limiter.limit("10/minute")
def actualizar(
    request: Request,
    criterio_id: int,
    data: CriterioEvaluacionUpdate,
    db: Session = Depends(get_db),
):
    if not request.state.user.is_teacher:
        raise HTTPException(
            status_code=403, detail="Solo profesores pueden modificar criterios"
        )
    return evaluacion_controller.actualizar_criterio(db, criterio_id, data)


@router.delete("/{criterio_id}")
@limiter.limit("10/minute")
def eliminar(request: Request, criterio_id: int, db: Session = Depends(get_db)):
    if not request.state.user.is_teacher:
        raise HTTPException(
            status_code=403, detail="Solo profesores pueden eliminar criterios"
        )
    return evaluacion_controller.eliminar_criterio(db, criterio_id)


@router.get("/aula/{aula_id}", response_model=List[CriterioEvaluacionOut])
@limiter.limit("30/minute")
def listar_por_aula(request: Request, aula_id: int, db: Session = Depends(get_db)):
    return evaluacion_controller.listar_criterios(db, aula_id)
