from pydantic import BaseModel
from typing import Optional


# Esquema para mostrar datos de un usuario (cuando respondes al frontend)
class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    is_teacher: bool

    class Config:
        from_attibutes = True


class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str
    is_teacher: bool = False

    class Config:
        from_attibutes = True


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attibutes = True


class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        from_attibutes = True


class UserAuth(BaseModel):
    id: int
    is_teacher: Optional[bool]
