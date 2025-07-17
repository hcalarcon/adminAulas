from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal


class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    fecha_creacion: date
    fecha_limite: Optional[date] = None
    aula_id: int
    created_by: int
    alumno_id: Optional[int] = None  # si es individual


class TareaCreate(TareaBase):
    pass


class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    fecha_limite: Optional[date] = None
    alumno_id: Optional[int] = None


class TareaOut(TareaBase):
    id: int
    cantidad_alumnos: Optional[int] = None
    entregados: Optional[int] = None

    class Config:
        from_attributes = True
