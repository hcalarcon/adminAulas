from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class ClaseBase(BaseModel):

    class Config:
        from_attibutes = True


class Clase(ClaseBase):

    tema: str
    fecha: date
    aula_id: int


class ClaseCreate(Clase):
    fecha: date
    aula_id: int


class ClaseOut(Clase):
    id: int
    fecha: date
    aula_id: int
    grupo_id: Optional[int] = None
    cuatrimestre: int


class ClaseUpdate(Clase):
    tema: Optional[str] = None
    fecha: Optional[date] = None
    aula_id: Optional[int] = None


class ClaseMasivaCreate(BaseModel):
    tema: str
    fecha: date
    grupo_id: Optional[int] = None
    cuatrimestre: int


class ClasesMasivasRequest(BaseModel):
    aula_id: int
    clases: List[ClaseMasivaCreate]
