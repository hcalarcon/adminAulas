from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from src.database.baseClass import Base


class Asistencia(Base):

    alumno_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    clase_id = Column(Integer, ForeignKey("clase.id"), primary_key=True)

    presente = Column(Integer, nullable=False)  # 1: presente, 2: ausente, 3: tarde
    justificado = Column(String, nullable=True)

    alumno = relationship("Usuarios", back_populates="asistencias")
    clase = relationship("Clase", back_populates="asistencias")
