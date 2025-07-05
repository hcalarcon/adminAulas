from fastapi import Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi import FastAPI
from src.security import auth
from src.modules.usuarios.user_schemas import UserAuth

# Definimos un esquema de seguridad para OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Middleware para validar el token
async def decode_token_from_request(request: Request):

    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Limpiar el token si tiene el prefijo "Bearer"
        token = token.split(" ")[1] if " " in token else token

        # Decodificamos el token usando la clave secreta
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])

        # Extraemos el id del usuario desde el payload
        user_id = payload.get("sub")
        is_teacher = payload.get("is_teacher")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        response = request.state.user = UserAuth(id=user_id, is_teacher=is_teacher)
        return response

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
