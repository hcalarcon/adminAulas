from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from src.core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.security import security
from src.models.user_model import Usuarios


load_dotenv()


# Clave secreta y algoritmo
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()  # copiamos los datos

    if expires_delta:  # si hay tiempo, se calcula cuando expira
        expire = datetime.now(timezone.utc) + expires_delta
    else:  # si no, expira en 15 minutos
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#


def login(db: Session, email: str, password: str):
    db_user = db.query(Usuarios).filter(Usuarios.email == email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="El correo no existe")

    pass_hash = security.verify_password(password, db_user.password)

    if not pass_hash:
        raise HTTPException(status_code=400, detail="Contra incorrecta")

    access_token = create_access_token(
        data={"sub": str(db_user.id), "is_teacher": db_user.is_teacher},
        expires_delta=timedelta(minutes=3600),
    )

    return {
        "user": {
            "id": db_user.id,
            "nombre": db_user.nombre,
            "apellido": db_user.apellido,
            "email": db_user.email,
            "is_teacher": db_user.is_teacher,
            "cambiarContrasena": db_user.cambiarContrasena,
        },
        "access_token": access_token,
    }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
