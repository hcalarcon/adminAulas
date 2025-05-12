from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from src.database.baseClass import Base
from src.models.asistencia_model import Asistencia


class Clase(Base):

    id = Column(Integer, primary_key=True, index=True)
    aula_id = Column(Integer, ForeignKey("aula.id"), nullable=False)
    tema = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)

    aula = relationship("Aula", back_populates="clases")
    asistencias = relationship("Asistencia", back_populates="clase")
