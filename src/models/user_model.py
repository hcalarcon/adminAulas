from sqlalchemy import Column, Integer, String, Boolean
from src.database.baseClass import Base
from sqlalchemy.orm import relationship
from src.models.aulas_model import Aula
from src.models.alarcoins_model import Alarcoin


class Usuarios(Base):

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_teacher = Column(Boolean, default=False)
    cambiarContrasena = Column(Boolean, default=True)

    aulas = relationship(
        "Aula", back_populates="profesor", foreign_keys=[Aula.profesor_id]
    )
    aulas_inscripto = relationship(
        "Aula", secondary="alumnos_aulas", back_populates="alumnos"
    )
    asistencias = relationship("Asistencia", back_populates="alumno")
    alarcoins = relationship(
        "Alarcoin", back_populates="alumno", cascade="all, delete-orphan"
    )
