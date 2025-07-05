from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from src.modules.usuarios.user_schemas import Usuario


class AulaBase(BaseModel):
    class Config:
        from_attributes = True


class Aula(AulaBase):
    id: int
    nombre: str
    ano: int
    division: int
    especialidad: str
    profesor_id: Optional[int]
    tipo: str


class AulaCreate(Aula):
    nombre: str
    ano: int
    division: int
    especialidad: str
    tipo: str
    profesor_id: Optional[int] = None


class AulaOut(Aula):
    id: int
    nombre: str
    ano: int
    division: int
    especialidad: str
    profesor_id: Optional[int] = None
    tipo: str


class AulaUpdate(Aula):
    nombre: Optional[str] = None
    ano: Optional[int] = None
    division: Optional[int] = None
    especialidad: Optional[str] = None
    profesor_id: Optional[int] = None


class AsignarProfesor(Aula):
    id: int
    nombre: str
    ano: int
    division: int
    especialidad: str
    profesor_id: int


class AlumnosAsignacion(AulaBase):

    alumnos_ids: List[int]


class Clase(BaseModel):
    topic: str
    date: date


class AulaConCantidadClases(Aula):
    cantidad_clases: int


class AulaConAlumnosResponse(Aula):
    id: int
    nombre: str
    ano: int
    division: int
    especialidad: str
    cantidad_clases: Optional[int] = None
    alumnos: List[Usuario] = None
    profesor_id: Optional[int] = None
