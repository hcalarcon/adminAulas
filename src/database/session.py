from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
import logging


try:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logging.error(f"Error al conectar con la base de datos: {e}")
    sessionLocal = None
