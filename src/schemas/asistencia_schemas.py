from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class AsistenciaBase(BaseModel):
    alumno_id: int
    presente: int
    justificado: Optional[str]


class AsistenciaCreate(AsistenciaBase):
    pass


class AsistenciaOut(AsistenciaBase):
    pass


class AsistenciaUpdate(AsistenciaBase):
    presente: Optional[int] = None
    justificado: Optional[str] = None


class AsistenciaPorAula(BaseModel):
    alumno_id: int
    alumno_nombre: str  # Puedes agregar el nombre del alumno si lo tienes
    presente: int
    justificado: Optional[str] = None
    porcentaje_asistencia: float  # Porcentaje de asistencia de este alumno


class AsistenciaPorAulaOut(BaseModel):
    aula_id: int
    asistencias: List[AsistenciaPorAula]
    porcentaje_aula: float  # Porcentaje de asistencia para todo el aula


class AlumnoAsistenciaResumen(BaseModel):
    alumno_id: int
    alumno_nombre: str
    porcentaje_asistencia: float


class AsistenciasAulaResumenOut(BaseModel):
    aula_id: int
    asistencias: List[AlumnoAsistenciaResumen]
    porcentaje_aula: float


class AsistenciaDetalle(BaseModel):
    fecha: date
    clase_nombre: str
    presente: int
    justificado: Optional[str] = None


class AsistenciaAlumno(BaseModel):
    alumno_id: int
    asistencias: List[AsistenciaDetalle]
    porcentaje_asistencia: float
