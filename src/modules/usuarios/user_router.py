from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from src.api.deps import get_db
from src.modules.usuarios import user_controller as userCrud
from src.modules.usuarios import user_schemas
from src.security.auth import login, refresh_token_controller
from src.core.limiter import limiter

router = APIRouter()


@router.get("/", response_model=List[user_schemas.Usuario])
@limiter.limit("30/minute")
def get_users(request: Request, db: Session = Depends(get_db)):
    return userCrud.get_user(db)


@router.post("/", response_model=user_schemas.Usuario)
@limiter.limit("10/minute")
def create_users(
    request: Request, usuario: user_schemas.UsuarioCreate, db: Session = Depends(get_db)
):
    return userCrud.create_usuario(db, usuario=usuario)


@router.get("/me", response_model=user_schemas.Usuario)
@limiter.limit("30/minute")
def get_user(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    return userCrud.get_user_by_id(db, user.id)


@router.put("/me", response_model=user_schemas.Usuario)
@limiter.limit("10/minute")
def updata_user(
    request: Request, usuario: user_schemas.UsuarioUpdate, db: Session = Depends(get_db)
):
    user_id = request.state.user.id
    return userCrud.update_user(db, user_id, usuario=usuario)


@router.delete("/me", response_model=user_schemas.Usuario)
@limiter.limit("10/minute")
def delete_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    return userCrud.delete_user(db, user_id)


@router.post("/login", response_model=user_schemas.LoginOut)
@limiter.limit("5/minute")  # Más estricto para proteger contra fuerza bruta
def login_user(
    request: Request,
    login_data: user_schemas.LoginRequest,
    db: Session = Depends(get_db),
):
    return login(db, email=login_data.email, password=login_data.password)


@router.post("/refresh")
def refresh_token(data: user_schemas.RefreshRequest):

    return refresh_token_controller(data.refresh_token)
