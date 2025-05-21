from sqlalchemy.orm import Session
from src.models.user_model import Usuarios
from src.schemas import user_schemas
from fastapi import HTTPException
from src.security import security


def get_user(db: Session):
    return db.query(Usuarios).order_by(Usuarios.id).all()


def create_usuario(db: Session, usuario: user_schemas.UsuarioCreate):
    # Verificar si el usuario con ese correo ya existe
    # db_usuario = db.query(Usuarios).filter(Usuarios.email == usuario.email).first()
    db_usuario = existe(db, usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    pass_user = security.hash_password(usuario.password)

    # Crear un nuevo objeto Usuarios con los datos del usuario
    new_usuario = Usuarios(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        password=pass_user,
        is_teacher=usuario.is_teacher,
    )

    # Guardar el nuevo usuario en la base de datos
    db.add(new_usuario)
    db.commit()  # Hacer commit para guardar en la base de datos
    db.refresh(
        new_usuario
    )  # Refrescar el objeto con los datos actualizados (incluyendo el ID generado)

    return new_usuario


def get_user_by_id(db: Session, id: int):
    db_user = db.query(Usuarios).filter(Usuarios.id == id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="El usuario no existe")
    return db_user


def update_user(db: Session, id: int, usuario: user_schemas.UsuarioUpdate):
    db_user = existe(db, id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail="El usuario no existe")
    if usuario.email and usuario.email != db_user.email:
        if existe(db, email=usuario.email):
            raise HTTPException(status_code=400, detail="El correo ya está en uso")

    if usuario.nombre is not None:
        db_user.nombre = usuario.nombre
    if usuario.apellido is not None:
        db_user.apellido = usuario.apellido
    if usuario.email is not None:
        db_user.email = usuario.email
    if usuario.password is not None:
        pass_user = security.hash_password(usuario.password)
        db_user.password = pass_user

    if usuario.cambiarContrasena is not None:
        db_user.cambiarContrasena = usuario.cambiarContrasena

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, id: int):

    db_user = existe(db, id=id)

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(db_user)
    db.commit()
    return db_user


# funciones privadas
def existe(db: Session, email: str = None, id: int = None):
    query = db.query(Usuarios)
    if email:
        return query.filter(Usuarios.email == email).first()
    elif id:
        return query.filter(Usuarios.id == id).first()
    return None
