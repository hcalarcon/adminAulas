from pydantic import BaseModel
from typing import Optional


# Esquema para mostrar datos de un usuario (cuando respondes al frontend)
class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    is_teacher: bool
    grupo_id: Optional[int] = None
    cambiarContrasena: bool

    class Config:
        from_attributes = True


class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str
    is_teacher: bool = False
    cambiarContrasena: bool = True

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    cambiarContrasena: Optional[bool] = None
    grupo_id: Optional[str] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    id: int
    is_teacher: Optional[bool]


class LoginOut(BaseModel):
    user: Usuario
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True


class UsuarioConGrupo(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    is_teacher: bool
    cambiarContrasena: bool
    grupo_id: Optional[int]
    grupo_nombre: Optional[str]

    class Config:
        from_attributes = True


class RefreshRequest(BaseModel):
    refresh_token: str
