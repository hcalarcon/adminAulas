from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api.deps import get_db
from src.schemas import aula_schemas as aulas_schemas
from src.controllers import aulas_controller as aulas_crud
from src.schemas import user_schemas as user_schemas

router = APIRouter()


@router.get("/mis-aulas", response_model=List[aulas_schemas.AulaConCantidadClases])
def get_mis_aulas(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user.id
    return aulas_crud.get_aulas_por_profesor(db, user_id)


@router.put("/remover-profesor/{aula_id}", response_model=aulas_schemas.AulaUpdate)
def remover_profesor_de_aula(
    aula_id: int, request: Request, db: Session = Depends(get_db)
):
    user_id = request.state.user_id
    return aulas_crud.remover_profesor(db, aula_id, user_id)


@router.post("/{id}/alumnos/{alumno_id}", response_model=aulas_schemas.AulaUpdate)
def asignar_alumno_a_aula(id: int, alumno_id: int, db: Session = Depends(get_db)):
    return aulas_crud.asignar_alumno_a_aula(db, id, alumno_id)


@router.post("/{id}/alumnos", response_model=aulas_schemas.AulaUpdate)
def asignar_alumnos_a_aula(
    id: int, alumnos_ids: aulas_schemas.AlumnosAsignacion, db: Session = Depends(get_db)
):
    return aulas_crud.asignar_alumnos_a_aula(db, id, alumnos_ids.alumnos_ids)


@router.delete("/{id}/alumnos/{alumno_id}", response_model=aulas_schemas.AulaUpdate)
def eliminar_alumno_de_aula(id: int, alumno_id: int, db: Session = Depends(get_db)):
    return aulas_crud.eliminar_alumno_de_aula(db, id, alumno_id)


@router.delete("/{id}/alumnos", response_model=aulas_schemas.AulaUpdate)
def eliminar_alumnos_de_aula(
    id: int, alumnos_ids: List[int], db: Session = Depends(get_db)
):
    return aulas_crud.eliminar_alumnos_de_aula(db, id, alumnos_ids)


@router.get("/{aula_id}/alumnos", response_model=List[user_schemas.Usuario])
def obtener_alumnos_de_aula(aula_id: int, db: Session = Depends(get_db)):
    return aulas_crud.obtener_alumnos_de_aula(db, aula_id)


@router.get(
    "/mis-aulas-con-alumnos", response_model=List[aulas_schemas.AulaConAlumnosResponse]
)
def obtener_mis_aulas_con_alumnos(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(
            status_code=403, detail="No tienes permiso para ver esta información."
        )

    return aulas_crud.get_aulas_con_alumnos_por_profesor(db, user.id)


@router.get("/", response_model=List[aulas_schemas.Aula])
def get_aulas(request: Request, db: Session = Depends(get_db)):
    return aulas_crud.get_aula(db)


@router.post("/", response_model=aulas_schemas.AulaOut)
def create_aulas(aula: aulas_schemas.AulaCreate, db: Session = Depends(get_db)):
    return aulas_crud.crear_aula(db, aula)


@router.get("/{id}", response_model=aulas_schemas.Aula)
def get_aula(id: int, db: Session = Depends(get_db)):
    return aulas_crud.get_aula_by_id(db, id)


@router.put("/{id}", response_model=aulas_schemas.Aula)
def update_aula(id: int, aula: aulas_schemas.AulaUpdate, db: Session = Depends(get_db)):
    return aulas_crud.update_aula(db, aula, id)


@router.delete("/{id}", response_model=aulas_schemas.AulaOut)
def delete_aula(id: int, db: Session = Depends(get_db)):
    return aulas_crud.delete_aula(db, id=id)


@router.put("/{aula_id}/asignar-profesor", response_model=aulas_schemas.AsignarProfesor)
def asignar_profesor_a_aula(
    aula_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.state.user_id  # El profesor autenticado
    return aulas_crud.asignar_profesor(db, aula_id, user_id)
