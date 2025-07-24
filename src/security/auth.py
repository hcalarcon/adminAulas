from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from src.core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.security import security
from src.modules.usuarios.user_model import Usuarios

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


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = (
        datetime.now(timezone.utc) + expires_delta
    )  # Usamos UTC como en access_token
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login(db: Session, email: str, password: str):
    db_user = db.query(Usuarios).filter(Usuarios.email == email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="El correo no existe")

    pass_hash = security.verify_password(password, db_user.password)

    if not pass_hash:
        raise HTTPException(status_code=400, detail="Contra incorrecta")

    access_token = create_access_token(
        data={"sub": str(db_user.id), "is_teacher": db_user.is_teacher},
        expires_delta=timedelta(minutes=30),  # o menos
    )

    refresh_token = create_refresh_token(
        data={"sub": str(db_user.id)}, expires_delta=timedelta(days=7)  # más tiempo
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
        "refresh_token": refresh_token,
    }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def refresh_token_controller(refresh_token: str):
    try:

        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido")

        user_id = payload.get("sub")
        is_teacher = payload.get("is_teacher")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        new_access_token = create_access_token(
            data={"sub": user_id, "is_teacher": is_teacher},
            expires_delta=timedelta(minutes=60),
        )
        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
