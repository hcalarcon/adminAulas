from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.controllers import grupos_controller
from src.schemas import grupos_schemas
from src.security.auth import login
from src.core.limiter import limiter

router = APIRouter()


def verificar_profesor(request: Request):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")


@router.post("/", response_model=grupos_schemas.GrupoResponse)
@limiter.limit("10/minute")
def crear_grupo(
    request: Request,
    datos: grupos_schemas.GrupoCreate,
    db: Session = Depends(get_db),
):
    verificar_profesor(request)
    return grupos_controller.crear_grupo(db, datos)


@router.get("/", response_model=list[grupos_schemas.GrupoResponse])
@limiter.limit("10/minute")
def listar_grupos(
    request: Request,
    aula_id: int = None,
    db: Session = Depends(get_db),
):
    verificar_profesor(request)
    return grupos_controller.listar_grupos(db, aula_id)


@router.put("/", response_model=list[grupos_schemas.GrupoResponse])
@limiter.limit("10/minute")
def actualizar_grupos(
    request: Request,
    grupos: list[grupos_schemas.GrupoUpdate],
    db: Session = Depends(get_db),
):
    verificar_profesor(request)
    return grupos_controller.actualizar_grupos(db, grupos)


@router.delete("/", status_code=204)
@limiter.limit("10/minute")
def eliminar_grupos(
    request: Request,
    ids: list[int],
    db: Session = Depends(get_db),
):
    verificar_profesor(request)
    grupos_controller.eliminar_grupos(db, ids)


@router.post("/asignar-alumnos", response_model=grupos_schemas.GrupoResponse)
@limiter.limit("10/minute")
def asignar_alumnos(
    request: Request,
    data: grupos_schemas.AsignarAlumnosSchema,
    db: Session = Depends(get_db),
):
    verificar_profesor(request)
    return grupos_controller.asignar_alumnos(db, data)


@router.post("/eliminar-alumnos", response_model=grupos_schemas.GrupoResponse)
@limiter.limit("10/minute")
def eliminar_alumnos(
    request: Request,
    data: grupos_schemas.EliminarAlumnosSchema,
    db: Session = Depends(get_db),
):
    verificar_profesor(request)
    return grupos_controller.eliminar_alumnos_de_grupo(db, data)


@router.post(
    "/{grupo_id}/asignar-aula/{aula_id}", response_model=grupos_schemas.GrupoResponse
)
@limiter.limit("10/minute")
def asignar_aula_a_grupo(
    grupo_id: int,
    aula_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.state.user
    if not user.is_teacher:
        raise HTTPException(status_code=403, detail="Solo disponible para profesores")

    return grupos_controller.asignar_aula_a_grupo(db, grupo_id, aula_id)
