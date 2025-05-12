from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from src.api.deps import get_db
from src.controllers import user_controller as userCrud
from src.schemas import user_schemas as user_schemas
from src.security.auth import login

router = APIRouter()


@router.get("/", response_model=List[user_schemas.Usuario])
def get_users(request: Request, db: Session = Depends(get_db)):
    # user_id = request.state.user_id  # user_id para enviar al controlador
    return userCrud.get_user(db)


@router.post("/", response_model=user_schemas.Usuario)
def create_users(usuario: user_schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return userCrud.create_usuario(db, usuario=usuario)


@router.get("/me", response_model=user_schemas.Usuario)
def get_user(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    return userCrud.get_user_by_id(db, user.id)


@router.put("/me", response_model=user_schemas.Usuario)
def updata_user(
    request: Request, usuario: user_schemas.UsuarioUpdate, db: Session = Depends(get_db)
):
    user_id = request.state.user.id
    return userCrud.update_user(db, user_id, usuario=usuario)


@router.delete("/me", response_model=user_schemas.Usuario)
def delete_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    return userCrud.delete_user(db, user_id)


@router.post("/login")
def login_user(request: user_schemas.LoginRequest, db: Session = Depends(get_db)):
    return login(db, email=request.email, password=request.password)
