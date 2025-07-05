from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from src.database.baseClass import Base


class Configuracion(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    tipo_evaluacion = Column(String, default="inversa")  # inversa o tradicional
    dark_mode = Column(Boolean, default=False)
    color_primario = Column(String, default="#E814F0")  #
    foto_perfil_url = Column(String, nullable=True)
    escala_evaluacion = Column(Integer, default=100)  # opciones típicas: 10 o 100

    user = relationship("Usuarios", back_populates="configuracion")
