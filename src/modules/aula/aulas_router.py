from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api.deps import get_db
from src.modules.aula import aula_schemas as aulas_schemas
from src.modules.aula import aulas_controller as aulas_crud
from src.modules.usuarios import user_schemas as user_schemas
from src.core.limiter import limiter

router = APIRouter()


@router.get("/mis-aulas")
@limiter.limit("30/minute")
def get_mis_aulas(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    if not user.is_teacher:
        return aulas_crud.get_aulas_por_alumno(db, user.id)
    return aulas_crud.get_aulas_por_profesor(db, user.id)


@router.put("/remover-profesor/{aula_id}", response_model=aulas_schemas.AulaUpdate)
@limiter.limit("10/minute")
def remover_profesor_de_aula(
    aula_id: int, request: Request, db: Session = Depends(get_db)
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    user_id = user.id
    return aulas_crud.remover_profesor(db, aula_id, user_id)


@router.post("/{id}/alumnos/{alumno_id}", response_model=aulas_schemas.AulaUpdate)
@limiter.limit("10/minute")
def asignar_alumno_a_aula(
    id: int, alumno_id: int, request: Request, db: Session = Depends(get_db)
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.asignar_alumno_a_aula(db, id, alumno_id)


@router.post("/{id}/alumnos", response_model=aulas_schemas.AulaUpdate)
@limiter.limit("10/minute")
def asignar_alumnos_a_aula(
    id: int,
    alumnos_ids: aulas_schemas.AlumnosAsignacion,
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.asignar_alumnos_a_aula(db, id, alumnos_ids.alumnos_ids)


@router.delete("/{id}/alumnos/{alumno_id}", response_model=aulas_schemas.AulaUpdate)
@limiter.limit("10/minute")
def eliminar_alumno_de_aula(
    id: int, alumno_id: int, request: Request, db: Session = Depends(get_db)
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.eliminar_alumno_de_aula(db, id, alumno_id)


@router.delete("/{id}/alumnos", response_model=aulas_schemas.AulaUpdate)
@limiter.limit("10/minute")
def eliminar_alumnos_de_aula(
    id: int, alumnos_ids: List[int], request: Request, db: Session = Depends(get_db)
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.eliminar_alumnos_de_aula(db, id, alumnos_ids)


@router.get("/{aula_id}/alumnos", response_model=List[user_schemas.Usuario])
@limiter.limit("30/minute")
def obtener_alumnos_de_aula(
    aula_id: int, request: Request, db: Session = Depends(get_db)
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.obtener_alumnos_de_aula(db, aula_id)


@router.get(
    "/mis-aulas-con-alumnos", response_model=List[aulas_schemas.AulaConAlumnosResponse]
)
@limiter.limit("30/minute")
def obtener_mis_aulas_con_alumnos(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.get_aulas_con_alumnos_por_profesor(db, user.id)


@router.get("/", response_model=List[aulas_schemas.Aula])
@limiter.limit("30/minute")
def get_aulas(request: Request, db: Session = Depends(get_db)):
    return aulas_crud.get_aula(db)


@router.post("/", response_model=aulas_schemas.AulaOut)
@limiter.limit("10/minute")
def create_aulas(
    aula: aulas_schemas.AulaCreate, request: Request, db: Session = Depends(get_db)
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.crear_aula(db, aula)


@router.get("/{id}", response_model=aulas_schemas.Aula)
@limiter.limit("30/minute")
def get_aula(id: int, request: Request, db: Session = Depends(get_db)):
    return aulas_crud.get_aula_by_id(db, id)


@router.put("/{id}", response_model=aulas_schemas.Aula)
@limiter.limit("10/minute")
def update_aula(
    id: int,
    aula: aulas_schemas.AulaUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.update_aula(db, aula, id)


@router.delete("/{id}", response_model=aulas_schemas.AulaOut)
@limiter.limit("10/minute")
def delete_aula(id: int, request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.delete_aula(db, id=id)


@router.put("/{aula_id}/asignar-profesor", response_model=aulas_schemas.AsignarProfesor)
@limiter.limit("10/minute")
def asignar_profesor_a_aula(
    aula_id: int, request: Request, db: Session = Depends(get_db)
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return aulas_crud.asignar_profesor(db, aula_id, user.id)
