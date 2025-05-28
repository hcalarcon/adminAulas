from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from fastapi import HTTPException, status

# Crea el contexto de cifrado con el algoritmo bcrypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str) -> str:
#     """Devuelve el hash de una contraseña en texto plano."""
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verifica que una contraseña en texto plano coincida con su hash."""
#     try:
#         return pwd_context.verify(plain_password, hashed_password)
#     except UnknownHashError:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="La contraseña no está en un formato válido.",
#         )

from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Devuelve el hash de una contraseña en texto plano."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que una contraseña en texto plano coincida con su hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El hash de la contraseña no es reconocible o está dañado.",
        )
    except Exception as e:
        print(f"[verify_password] Error al verificar contraseña: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Error interno al verificar la contraseña.",
        )
