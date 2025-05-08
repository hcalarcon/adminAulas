#Generamos la conexion con la base de datos

from typing import Generator
from src.database.session import sessionLocal

def get_db()-> Generator:
    db= sessionLocal()
    try:
        yield db
    finally:
        db.close()