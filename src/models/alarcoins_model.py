from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from src.database.baseClass import Base


class Alarcoin(Base):

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)  # Puede ser positivo o negativo
    detalle = Column(String, nullable=True)
    fecha = Column(Date, nullable=False)
    suma = Column(Boolean, default=True)  # True: suma, False: resta

    alumno_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    alumno = relationship("Usuarios", back_populates="alarcoins")

    aula_id = Column(Integer, ForeignKey("aula.id"), nullable=False)
    aula = relationship("Aula", back_populates="alarcoins")
