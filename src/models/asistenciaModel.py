from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from src.database.baseClass import Base


class Asistencia(Base):

    alumno_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    clase_id = Column(Integer, ForeignKey("clase.id"), primary_key=True)
    presente = Column(Boolean, default=False)

    alumno = relationship("Usuarios", back_populates="asistencias")
    clase = relationship("Clase", back_populates="asistencias")
