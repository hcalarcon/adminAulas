from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class AlarcoinBase(BaseModel):
    cantidad: int
    detalle: Optional[str] = None
    fecha: Optional[date] = None
    suma: Optional[int] = None

    class Config:
        from_attributes = True


class AlarcoinCreate(AlarcoinBase):
    alumno_id: int
    aula_id: int


class AlarcoinOut(AlarcoinBase):
    id: int


class AlumnoAlarcoinOut(BaseModel):
    id: int
    alarcoins: List[AlarcoinOut]


class AulaAlarcoinOut(BaseModel):
    aula_id: int
    nombre: str
    alumnos: List[AlumnoAlarcoinOut]


class AulaAlarcoinAlumnoOut(BaseModel):
    aula_id: int
    nombre: str
    alarcoins: List[AlarcoinOut]
