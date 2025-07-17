from pydantic import BaseModel, Field
from typing import Literal


class CriterioEvaluacionBase(BaseModel):
    criterio: Literal["evaluacion", "asistencia", "trabajos", "actitudinal"]
    peso: int = Field(ge=0, le=100)


class CriterioEvaluacionCreate(CriterioEvaluacionBase):
    aula_id: int


class CriterioEvaluacionUpdate(CriterioEvaluacionBase):
    pass


class CriterioEvaluacionOut(CriterioEvaluacionBase):
    id: int
    aula_id: int

    class Config:
        from_attributes = True
