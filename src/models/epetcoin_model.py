from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from src.database.baseClass import Base


class EpetCoin(Base):

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)  # ej: MartinezCoin
    profesor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    profesor = relationship("Usuarios", back_populates="monedas_creadas")
    transacciones = relationship("TransaccionCoin", back_populates="moneda")


class TransaccionCoin(Base):

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)  # Puede ser positivo o negativo
    detalle = Column(String, nullable=True)
    fecha = Column(Date, nullable=False)
    suma = Column(Boolean, default=True)  # True: suma, False: resta

    alumno_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    moneda_id = Column(Integer, ForeignKey("epetcoin.id"), nullable=False)
    aula_id = Column(Integer, ForeignKey("aula.id"), nullable=False)

    alumno = relationship("Usuarios", back_populates="coins_recibidos")
    moneda = relationship("EpetCoin", back_populates="transacciones")
    aula = relationship("Aula", back_populates="transacciones_coin")
