from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from decimal import Decimal


class NotaTareaBase(BaseModel):
    tarea_id: int
    alumno_id: int
    nota: Optional[Decimal] = 10.00
    fecha_entrega: Optional[date] = None
    entregado: Optional[bool] = False


class NotaTareaCreate(NotaTareaBase):
    pass


class NotaTareaUpdate(BaseModel):
    nota: Optional[Decimal] = None
    fecha_entrega: Optional[date] = None
    entregado: Optional[bool] = None


class NotaTareaOut(NotaTareaBase):
    id: int

    class Config:
        from_attributes = True


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
