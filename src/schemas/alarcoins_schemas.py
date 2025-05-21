from pydantic import BaseModel
from datetime import date
from typing import Optional


class AlarcoinBase(BaseModel):
    cantidad: int
    detalle: Optional[str] = None
    fecha: Optional[date] = None  # Si no se pasa, lo pone el modelo


class AlarcoinCreate(AlarcoinBase):
    alumno_id: int


class AlarcoinOut(AlarcoinBase):
    id: int
    alumno_id: int

    class Config:
        from_attributes = True  # O orm_mode = True si usás Pydantic <2
