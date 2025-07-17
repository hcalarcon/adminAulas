from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from src.api.deps import get_db
from typing import List
from src.modules.tarea.tarea_schemas import TareaCreate, TareaOut, TareaUpdate
from src.modules.tarea import tarea_controller
from src.core.limiter import limiter

router = APIRouter()


@router.post(
    "/",
)
@limiter.limit("10/minute")
def crear_tarea(
    request: Request,
    tarea: TareaCreate,
    db: Session = Depends(get_db),
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return tarea_controller.crear_tarea(db, tarea)


@router.get("/aula/{aula_id}", response_model=List[TareaOut])
@limiter.limit("20/minute")
def listar_tareas_por_aula(
    request: Request,
    aula_id: int,
    db: Session = Depends(get_db),
):
    return tarea_controller.listar_tareas_por_aula(db, aula_id)


@router.get("/me", response_model=list[TareaOut])
def tareas_por_usuario(request: Request, db: Session = Depends(get_db)):
    return tarea_controller.listar_tareas_por_usuario(db, request.state.user)


@router.get("/{tarea_id}", response_model=TareaOut)
@limiter.limit("20/minute")
def obtener_tarea(
    request: Request,
    tarea_id: int,
    db: Session = Depends(get_db),
):
    return tarea_controller.obtener_tarea(db, tarea_id)


@router.put("/{tarea_id}", response_model=TareaOut)
@limiter.limit("10/minute")
def actualizar_tarea(
    request: Request,
    tarea_id: int,
    tarea_data: TareaUpdate,
    db: Session = Depends(get_db),
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return tarea_controller.actualizar_tarea(db, tarea_id, tarea_data)


@router.delete("/{tarea_id}", response_model=dict)
@limiter.limit("5/minute")
def eliminar_tarea(
    request: Request,
    tarea_id: int,
    db: Session = Depends(get_db),
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return tarea_controller.eliminar_tarea(db, tarea_id)
