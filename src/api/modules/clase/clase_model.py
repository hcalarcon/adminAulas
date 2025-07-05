from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from src.database.baseClass import Base
from modules.asistencia.asistencia_model import Asistencia
from modules.grupos.grupos_model import Grupos


class Clase(Base):

    id = Column(Integer, primary_key=True, index=True)
    aula_id = Column(Integer, ForeignKey("aula.id"), nullable=False)
    tema = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    cuatrimestre = Column(Integer)

    aula = relationship("Aula", back_populates="clases")
    asistencias = relationship("Asistencia", back_populates="clase")

    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=True)
    grupo = relationship("Grupos")
