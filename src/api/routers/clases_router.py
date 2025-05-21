# routes/clasesRouter.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.schemas import clases_schemas
from src.controllers import clase_controller
from typing import List

router = APIRouter()


@router.post("/masivas", response_model=List[clases_schemas.ClaseOut])
def crear_clases_masivas(
    request: clases_schemas.ClasesMasivasRequest, db: Session = Depends(get_db)
):
    return clase_controller.crear_clases_masivas(
        db, request.aula_id, [clase.model_dump() for clase in request.clases]
    )


# agregar eliminacion masiva


# agregar filtros
@router.get("/aulas/{aula_id}/clases", response_model=List[clases_schemas.ClaseOut])
def get_clases_por_aula(aula_id: int, db: Session = Depends(get_db)):
    return clase_controller.obtener_clases_por_aula(db, aula_id)


@router.post("/", response_model=clases_schemas.ClaseOut)
def crear_clase(clase: clases_schemas.ClaseCreate, db: Session = Depends(get_db)):
    return clase_controller.crear_clase(db, clase)


@router.put("/{id}", response_model=clases_schemas.ClaseOut)
def actualizar_clase(
    id: int, clase: clases_schemas.ClaseUpdate, db: Session = Depends(get_db)
):
    return clase_controller.actualizar_clase(db, id, clase)


@router.delete("/{id}", response_model=clases_schemas.ClaseOut)
def eliminar_clase(id: int, db: Session = Depends(get_db)):
    return clase_controller.eliminar_clase(db, id)


@router.get("/{id}", response_model=clases_schemas.ClaseOut)
def obtener_clase(id: int, db: Session = Depends(get_db)):
    return clase_controller.obtener_clase(db, id)
