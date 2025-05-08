from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings


engine = create_engine(settings.DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)