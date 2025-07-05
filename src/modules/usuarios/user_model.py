from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from src.database.baseClass import Base
from sqlalchemy.orm import relationship
from src.modules.aula.aulas_model import Aula
from src.modules.epetcoins.epetcoin_model import TransaccionCoin, EpetCoin
from src.modules.evaluacion.tarea_model import Tarea
from src.modules.usuarios.configuracion_model import Configuracion


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
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=True)
    grupo = relationship("Grupos", back_populates="alumnos")

    coins_recibidos = relationship("TransaccionCoin", back_populates="alumno")
    monedas_creadas = relationship("EpetCoin", back_populates="profesor")
    tareas_creadas = relationship(
        "Tarea",
        back_populates="creador",
        foreign_keys="[Tarea.created_by]",
    )

    tareas_asignadas = relationship(
        "NotaTarea", back_populates="alumno", cascade="all, delete-orphan"
    )

    configuracion = relationship("Configuracion", back_populates="user", uselist=False)
