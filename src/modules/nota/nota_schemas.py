from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Dict, Literal
from decimal import Decimal


class NotaTareaBase(BaseModel):
    tarea_id: int
    alumno_id: int
    nota: Optional[Decimal] = 10
    fecha_entrega: Optional[date] = None
    entregado: Optional[bool] = False


class NotaTareaCreate(NotaTareaBase):
    pass


class NotaTareaUpdate(BaseModel):
    alumno_id: int
    nota: Optional[Decimal] = None
    fecha_entrega: Optional[date] = None
    entregado: Optional[bool] = None


class NotaTareaUpdateMasiva(BaseModel):
    tarea_id: int
    notas: List[NotaTareaUpdate]


class NotaTareaOut(NotaTareaBase):
    id: int

    class Config:
        from_attributes = True


class NotaTareaEliminarMasiva(BaseModel):
    tarea_id: int
    alumno_ids: List[int]


# actitudinal
class NotaActitudinalBase(BaseModel):
    clase_id: int
    alumno_id: int
    nota: Decimal


class NotaActitudinalCreate(NotaActitudinalBase):
    pass


class NotaActitudinalUpdate(BaseModel):
    nota: Optional[Decimal] = None


class NotaActitudinalOut(NotaActitudinalBase):
    id: int

    class Config:
        from_attributes = True


class NotaTareaAsignacionMasiva(BaseModel):
    tarea_id: int
    alumnos: List[int]


class NotaPorCriterio(BaseModel):
    promedio: float
    peso: Decimal = Field(..., ge=0, le=100)
    contribucion: float


class NotaFinalInput(BaseModel):
    porcentaje_asistencia: float = Field(..., ge=0, le=100)


class NotaFinalOut(BaseModel):
    nota_final: float
    nota_sin_condiciones: float
    detalles: Dict[str, NotaPorCriterio]
    condiciones_fallidas: List[Literal["asistencia", "trabajos", "evaluacion"]]
