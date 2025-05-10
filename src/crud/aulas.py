from sqlalchemy.orm import Session
from src.models.aulasModel import Aula
from src.schemas import aulaSchemas
from fastapi import HTTPException
from src.utility.exist import existe
from src.models.userModel import Usuarios


def get_aula(db: Session):
    return db.query(Aula).all()


def crear_aula(db: Session, aula: aulaSchemas.AulaCreate):
    nueva_aula = Aula(
        nombre=aula.nombre,
        ano=aula.ano,
        division=aula.division,
        especialidad=aula.especialidad,
    )
    db.add(nueva_aula)
    db.commit()
    db.refresh(nueva_aula)
    return nueva_aula


def get_aula_by_id(db: Session, id: int):
    # db_aula = db.query(Aula).filter(Aula.id == id).first()
    db_aula = existe(db, Aula, id=id)
    if not db_aula:
        raise HTTPException(status_code=401, detail="El aula no existe")

    return db_aula


def update_aula(db: Session, aula: aulaSchemas.AulaUpdate, id: int):
    db_aula = get_aula_by_id(db, id)

    if aula.nombre is not None:
        db_aula.nombre = aula.nombre
    if aula.ano is not None:
        db_aula.ano = aula.ano
    if aula.division is not None:
        db_aula.division = aula.division
    if aula.especialidad is not None:
        db_aula.especialidad = aula.especialidad

    db.commit()
    db.refresh(db_aula)
    return db_aula


def delete_aula(db: Session, id: int):

    db_aula = db.query(Aula).filter(Aula.id == id).first()

    db.delete(db_aula)
    db.commit()
    return db_aula


def asignar_profesor(db: Session, aula_id: int, profesor_id: int):
    aula = existe(db, Aula, id=aula_id)
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    aula.profesor_id = profesor_id
    db.commit()
    db.refresh(aula)
    return aula


def get_aulas_por_profesor(db: Session, profesor_id: int):
    return db.query(Aula).filter(Aula.profesor_id == profesor_id).all()


def remover_profesor(db: Session, aula_id: int, profesor_id: int):
    aula = existe(db, Aula, id=aula_id)

    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    print(f"DEBUG -> aula.profesor_id: {aula.profesor_id}, user: {profesor_id}")

    if aula.profesor_id != int(profesor_id):
        raise HTTPException(
            status_code=403, detail="No puedes eliminar a otro profesor"
        )

    aula.profesor_id = None
    db.commit()
    db.refresh(aula)
    return aula


def asignar_alumno_a_aula(db: Session, aula_id: int, alumno_id: int):
    # Verifica que el aula exista
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    # Verifica que el alumno exista
    alumno = db.query(Usuarios).filter(Usuarios.id == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    if alumno in aula.alumnos:
        raise HTTPException(
            status_code=400, detail="El alumno ya está asignado a esta aula"
        )

    # Asigna al alumno a la materia
    aula.alumnos.append(alumno)
    db.commit()
    db.refresh(aula)
    return aula


# Asignar varios alumnos a un aula de manera masiva
def asignar_alumnos_a_aula(db: Session, aula_id: int, alumnos_ids: list):
    aula = existe(db, Aula, id=aula_id)
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    errores = []

    for alumno_id in alumnos_ids:
        alumno = db.query(Usuarios).filter(Usuarios.id == alumno_id).first()
        if not alumno:
            errores.append(f"Alumno con ID {alumno_id} no encontrado")
            continue

        if alumno in aula.alumnos:
            errores.append(f"Alumno con ID {alumno_id} ya está asignado al aula")
            continue

        aula.alumnos.append(alumno)

    db.commit()
    db.refresh(aula)

    if errores:
        raise HTTPException(
            status_code=400,
            detail={"asignados": [a.id for a in aula.alumnos], "errores": errores},
        )

    return aula


def obtener_alumnos_de_aula(db: Session, aula_id: int):
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    return aula.alumnos


# Eliminar un alumno de un aula
def eliminar_alumno_de_aula(db: Session, aula_id: int, alumno_id: int):
    # Verifica que el aula exista
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    # Verifica que el alumno exista
    alumno = db.query(Usuarios).filter(Usuarios.id == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # Elimina al alumno de la lista de alumnos
    if alumno not in aula.alumnos:
        raise HTTPException(
            status_code=404, detail="El alumno no está asignado a esta aula"
        )

    aula.alumnos.remove(alumno)
    db.commit()
    db.refresh(aula)
    return aula


# Eliminar varios alumnos de un aula
def eliminar_alumnos_de_aula(db: Session, aula_id: int, alumnos_ids: list):
    # Verifica que el aula exista
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    # Obtener los alumnos
    alumnos = db.query(Usuarios).filter(Usuarios.id.in_(alumnos_ids)).all()
    if len(alumnos) != len(alumnos_ids):
        raise HTTPException(status_code=404, detail="Uno o más alumnos no encontrados")

    # Elimina los alumnos de la materia
    for alumno in alumnos:
        if alumno in aula.alumnos:
            aula.alumnos.remove(alumno)
    db.commit()
    db.refresh(aula)
    return aula
