from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from src.database.baseClass import Base


class CriterioEvaluacion(Base):
    id = Column(Integer, primary_key=True)
    aula_id = Column(Integer, ForeignKey("aula.id"), nullable=False)
    criterio = Column(String, nullable=False)  # ej: "evaluacion", "asistencia"
    peso = Column(Numeric(5, 2), nullable=False)  # porcentaje entre 0 y 100

    aula = relationship("Aula", back_populates="criterios")
