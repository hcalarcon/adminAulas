from fastapi import APIRouter, Depends, Request, HTTPException
from src.modules.asistencia.asistencia_schemas import (
    AsistenciaCreate,
    AsistenciaOut,
    AsistenciaBase,
    AsistenciasAulaResumenOut,
    AsistenciaAlumno,
)
from src.modules.asistencia import asistencia_controller
from sqlalchemy.orm import Session
from src.api.deps import get_db
from typing import List
from src.core.limiter import limiter  # si usás limiter para control de peticiones

router = APIRouter()


@router.post("/", response_model=AsistenciaOut)
@limiter.limit("10/minute")
def crear_asistencia(
    request: Request, asistencia: AsistenciaCreate, db: Session = Depends(get_db)
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return asistencia_controller.registrar_asistencia(db, asistencia)


@router.post("/masiva/{clase_id}", response_model=List[AsistenciaOut])
@limiter.limit("10/minute")
def crear_asistencias_masivas(
    request: Request,
    clase_id: int,
    asistencias: List[AsistenciaCreate],
    db: Session = Depends(get_db),
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return asistencia_controller.registrar_asistencias_masivas(
        db, clase_id, asistencias
    )


@router.get("/mis-asistencias", response_model=List[AsistenciaAlumno])
@limiter.limit("30/minute")
def consultar_asistencia_alumno(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    # Este endpoint es para alumnos (o profesores que consultan su propia asistencia)
    return asistencia_controller.obtener_asistencias_por_alumno(db, user.id)


@router.get("/asistencias-por-clase/{clase_id}", response_model=List[AsistenciaBase])
@limiter.limit("30/minute")
def get_asistencias_clases(
    request: Request, clase_id: int, db: Session = Depends(get_db)
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="Usuario no autorizado")
    return asistencia_controller.obtener_asistencias_por_clase(db, clase_id)


@router.get("/alumno/{alumno_id}/{aula_id}", response_model=AsistenciaAlumno)
@limiter.limit("30/minute")
def consultar_asistencia(
    request: Request, alumno_id: int, aula_id: int, db: Session = Depends(get_db)
):
    if not request.state.user.is_teacher:
        raise HTTPException(status_code=403, detail="No autorizado")
    return asistencia_controller.obtener_asistencias_por_alumno(db, alumno_id, aula_id)


@router.get("/aula/{aula_id}", response_model=AsistenciasAulaResumenOut)
@limiter.limit("30/minute")
def obtener_asistencias(request: Request, aula_id: int, db: Session = Depends(get_db)):
    # Acá asumo que cualquiera puede consultar el resumen de asistencias de un aula.
    return asistencia_controller.obtener_asistencias_por_aula(db, aula_id)
