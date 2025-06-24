from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class EpetCoinBase(BaseModel):
    id: int
    nombre: str
    profesor_id: int


class TransaccionCoinBase(BaseModel):
    cantidad: int
    detalle: str
    suma: int
    cantidad: int
    alumno_id: int
    aula_id: int
    moneda_id: int

    class Config:
        from_attributes = True


class TransaccionCoinOut(BaseModel):
    id: int
    cantidad: int
    detalle: str
    fecha: date
    suma: bool


class AlumnoCoinOut(BaseModel):
    id: int
    coins: List[TransaccionCoinOut]


class AulaCoinOut(BaseModel):
    aula_id: int
    nombre: str
    epetcoins: List[AlumnoCoinOut]


class EpetCoinOut(BaseModel):
    nombre: str


# class AlarcoinBase(BaseModel):
#     cantidad: int
#     detalle: Optional[str] = None
#     fecha: Optional[date] = None
#     suma: Optional[int] = None

#     class Config:
#         from_attributes = True


# class AlarcoinCreate(AlarcoinBase):
#     alumno_id: int
#     aula_id: int


# class AlarcoinOut(AlarcoinBase):
#     id: int


# class AlumnoAlarcoinOut(BaseModel):
#     id: int
#     alarcoins: List[AlarcoinOut]


# class AulaAlarcoinOut(BaseModel):
#     aula_id: int
#     nombre: str
#     alumnos: List[AlumnoAlarcoinOut]


# class AulaAlarcoinAlumnoOut(BaseModel):
#     aula_id: int
#     nombre: str
#     alarcoins: List[AlarcoinOut]
