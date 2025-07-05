from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Numeric
from src.database.baseClass import Base
from sqlalchemy.orm import relationship
from src.modules.aula.aulas_model import Aula
from src.modules.evaluacion.nota_model import NotaTarea


class Tarea(Base):
    id = Column(Integer, primary_key=True, index=True)
    aula_id = Column(Integer, ForeignKey("aula.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # NUEVO: tarea individual opcional
    alumno_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    titulo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String, nullable=True)  # "teorico", "practico", "evaluacion"
    fecha_creacion = Column(Date, nullable=False)
    fecha_limite = Column(Date, nullable=True)

    aula = relationship("Aula", back_populates="tareas")
    creador = relationship(
        "Usuarios", back_populates="tareas_creadas", foreign_keys=[created_by]
    )
    notas = relationship("NotaTarea", back_populates="tarea", cascade="all, delete")
