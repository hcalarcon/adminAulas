from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from src.database.baseClass import Base


grupos_aulas = Table(
    "grupos_aulas",
    Base.metadata,
    Column("grupo_id", ForeignKey("grupos.id"), primary_key=True),
    Column("aula_id", ForeignKey("aula.id"), primary_key=True),
)


class Grupos(Base):

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    aulas = relationship("Aula", secondary="grupos_aulas", back_populates="grupos")
    alumnos = relationship("Usuarios", back_populates="grupo")
