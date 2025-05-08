from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from src.api.deps import get_db
from src.schemas import aulaSchemas as aulas_schemas
from src.crud import aulas as aulas_crud

router = APIRouter()


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
    return aulas_crud.update_aula(db, aula, id=id)


@router.delete("/{id}", response_model=aulas_schemas.AulaOut)
def delete_aula(id: int, db: Session = Depends(get_db)):
    return aulas_crud.delete_aula(db, id=id)
