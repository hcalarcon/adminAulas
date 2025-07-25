from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api.deps import get_db
from src.modules.nota import nota_controller
from src.modules.nota.nota_schemas import (
    NotaTareaOut,
    NotaTareaCreate,
    NotaTareaUpdate,
    NotaTareaAsignacionMasiva,
    NotaFinalOut,
    NotaFinalInput,
    NotaTareaEliminarMasiva,
    NotaTareaUpdateMasiva,
)
from src.core.limiter import limiter

router = APIRouter()


@router.post("/asignar-masiva", response_model=List[NotaTareaOut])
@limiter.limit("10/minute")
def asignar_tarea_masiva(
    request: Request,
    data: NotaTareaAsignacionMasiva,
    db: Session = Depends(get_db),
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return nota_controller.asignar_tarea_masiva(db, data)


@router.post("/", response_model=NotaTareaOut)
@limiter.limit("10/minute")
def asignar_tarea(
    request: Request, data: NotaTareaCreate, db: Session = Depends(get_db)
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return nota_controller.asignar_tarea(db, data)


@router.put("/{nota_id}", response_model=NotaTareaOut)
@limiter.limit("10/minute")
def actualizar_nota_tarea(
    nota_id: int,
    data: NotaTareaUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return nota_controller.actualizar_nota_tarea(db, nota_id, data)


@router.put("/tareas/notas/masiva", response_model=dict)
@limiter.limit("10/minute")
def put_notas_masiva(
    request: Request, data: NotaTareaUpdateMasiva, db: Session = Depends(get_db)
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return nota_controller.actualizar_notas_masiva(db, data)


@router.post("/notas-tareas/eliminar")
@limiter.limit("10/minute")
def eliminar_notas(
    request: Request, data: NotaTareaEliminarMasiva, db: Session = Depends(get_db)
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return nota_controller.eliminar_notas_masivas(db, data)


@router.delete("/{nota_id}")
@limiter.limit("10/minute")
def eliminar_nota_tarea(
    nota_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return nota_controller.eliminar_nota_tarea(db, nota_id)


@router.get("/alumno/{alumno_id}", response_model=List[NotaTareaOut])
@limiter.limit("20/minute")
def obtener_notas_por_alumno(
    alumno_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    # Si es profesor o el mismo alumno puede consultar
    user = request.state.user
    if not user.is_teacher and user.id != alumno_id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return nota_controller.obtener_notas_por_alumno(db, alumno_id)


@router.get("/me")
@limiter.limit("10/min")
def obtener_mis_notas(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    return nota_controller.obtener_notas_agrupadas_por_aula(db, user.id)


@router.get("/tarea/{tarea_id}", response_model=List[NotaTareaOut])
@limiter.limit("20/minute")
def obtener_notas_por_tarea(
    tarea_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return nota_controller.obtener_notas_por_tarea(db, tarea_id)


@router.get("/alumno/{alumno_id}/aula/{aula_id}", response_model=List[NotaTareaOut])
@limiter.limit("20/minute")
def obtener_notas_por_alumno_y_aula(
    alumno_id: int,
    aula_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return nota_controller.obtener_notas_por_alumno_y_aula(db, alumno_id, aula_id)


@router.post(
    "/alumno/{alumno_id}/aula/{aula_id}/nota-final", response_model=NotaFinalOut
)
@limiter.limit("10/minute")
def calcular_nota_final_post(
    alumno_id: int,
    aula_id: int,
    data: NotaFinalInput,
    request: Request,
    db: Session = Depends(get_db),
):

    return nota_controller.calcular_nota_final(
        db, alumno_id, aula_id, data.porcentaje_asistencia
    )
