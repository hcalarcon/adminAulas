from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class AulaBase(BaseModel):
    class Config:
        from_attibutes = True


class Aula(AulaBase):

    nombre: str
    ano: int
    division: int
    especialidad: str
    profesor_id: int


class AulaCreate(Aula):
    nombre: str
    ano: int
    division: int
    especialidad: str


class AulaOut(Aula):
    id: int
    nombre: str
    ano: int
    division: int
    especialidad: str


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


class SessionCreate(Clase):
    classroom_id: int


class SessionOut(Clase):
    id: int
    classroom_id: int

    class Config:
        from_attibutes = True


class Asistencia(BaseModel):
    student_id: int
    session_id: int
    present: bool


class AsistenciaOut(Asistencia):
    class Config:
        from_attibutes = True
