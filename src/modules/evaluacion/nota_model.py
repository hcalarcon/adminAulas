from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date, Numeric
from src.database.baseClass import Base
from sqlalchemy.orm import relationship


class NotaTarea(Base):
    id = Column(Integer, primary_key=True, index=True)
    tarea_id = Column(Integer, ForeignKey("tarea.id"), nullable=False)
    alumno_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    nota = Column(Numeric(4, 2), nullable=False, default=10)  # de 0 a 10
    fecha_entrega = Column(Date, nullable=True)
    entregado = Column(Boolean, default=False)

    tarea = relationship("Tarea", back_populates="notas")
    alumno = relationship("Usuarios", back_populates="tareas_asignadas")
