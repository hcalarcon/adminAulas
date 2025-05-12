from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from src.database.baseClass import Base
from src.models.clase_model import Clase

# Tabla intermedia para alumnos en aulas - un alumno puede estar en muchas clases y una clase puede tener muchos alumnos
alumnos_aulas = Table(
    "alumnos_aulas",
    Base.metadata,
    Column("alumno_id", ForeignKey("usuarios.id"), primary_key=True),
    Column("aula_id", ForeignKey("aula.id"), primary_key=True),
)


class Aula(Base):

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    profesor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    ano = Column(Integer, nullable=False)
    division = Column(Integer, nullable=False)
    especialidad = Column(String, nullable=False)

    profesor = relationship(
        "Usuarios", back_populates="aulas", foreign_keys=[profesor_id]
    )
    alumnos = relationship(
        "Usuarios", secondary=alumnos_aulas, back_populates="aulas_inscripto"
    )
    clases = relationship("Clase", back_populates="aula")
