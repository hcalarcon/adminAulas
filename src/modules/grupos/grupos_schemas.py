from typing import List, Optional
from pydantic import BaseModel


class GrupoBase(BaseModel):
    nombre: str
    aula_id: int

    class Config:
        from_attibutes = True


class GrupoCreate(GrupoBase):
    pass


class GrupoUpdate(BaseModel):
    id: int
    nombre: Optional[str]
    aula_id: Optional[int]

    class Config:
        from_attibutes = True


class GrupoResponse(BaseModel):
    id: int
    nombre: str


class AsignarAlumnosSchema(BaseModel):
    grupo_id: int
    alumnos_ids: List[int]

    class Config:
        from_attibutes = True


class EliminarAlumnosSchema(BaseModel):
    grupo_id: int
    alumnos_ids: List[int]

    class Config:
        from_attibutes = True
