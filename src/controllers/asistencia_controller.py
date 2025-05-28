from sqlalchemy.orm import Session, joinedload
from src.schemas.asistencia_schemas import (
    AsistenciaCreate,
    AsistenciaPorAula,
)
from src.models.asistencia_model import Asistencia
from src.models.clase_model import Clase
from src.models.aulas_model import Aula
from src.models.user_model import Usuarios as Alumno
from typing import List, Dict, Any
from fastapi import HTTPException


def registrar_asistencia(db: Session, asistencia_data: AsistenciaCreate):
    asistencia_existente = (
        db.query(Asistencia)
        .filter_by(
            alumno_id=asistencia_data.alumno_id, clase_id=asistencia_data.clase_id
        )
        .first()
    )

    # comprobar que el aula exista
    if asistencia_existente:
        raise HTTPException(status_code=400, detail="Asistencia ya registrada")

    asistencia = Asistencia(**asistencia_data.model_dump())
    db.add(asistencia)
    db.commit()
    db.refresh(asistencia)
    return asistencia


def registrar_asistencias_masivas(
    db: Session, clase_id: int, asistencias: List[AsistenciaCreate]
):
    resultados = []

    for asistencia_data in asistencias:
        asistencia = (
            db.query(Asistencia)
            .filter_by(alumno_id=asistencia_data.alumno_id, clase_id=clase_id)
            .first()
        )

        if asistencia:
            asistencia.presente = asistencia_data.presente
            asistencia.justificado = asistencia_data.justificado
            resultados.append(asistencia)
        else:
            nueva = Asistencia(
                alumno_id=asistencia_data.alumno_id,
                clase_id=clase_id,
                presente=asistencia_data.presente,
                justificado=asistencia_data.justificado,
            )
            db.add(nueva)
            resultados.append(nueva)

    db.commit()
    return resultados


def actualizar_asistencia(db: Session, asistencia_data: AsistenciaCreate):
    asistencia = (
        db.query(Asistencia)
        .filter_by(
            alumno_id=asistencia_data.alumno_id, clase_id=asistencia_data.clase_id
        )
        .first()
    )

    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")

    asistencia.presente = asistencia_data.presente
    asistencia.justificado = asistencia_data.justificado
    db.commit()
    db.refresh(asistencia)
    return asistencia


def obtener_asistencias_por_alumno(db: Session, alumno_id: int):
    # 1. Obtener aulas en las que está inscripto el alumno
    aulas = (
        db.query(Aula)
        .join(Aula.alumnos)  # relación many-to-many desde Aula hacia Alumno
        .outerjoin(Clase, Aula.id == Clase.aula_id)
        .filter(Alumno.id == alumno_id)
        .group_by(Aula.id)
        .all()
    )

    resultado = []

    for aula in aulas:
        clases = (
            db.query(Clase).filter(Clase.aula_id == aula.id).order_by(Clase.fecha).all()
        )
        clase_ids = [clase.id for clase in clases]

        if not clase_ids:
            continue

        asistencias = (
            db.query(Asistencia, Clase)
            .join(Clase, Asistencia.clase_id == Clase.id)
            .options(joinedload(Asistencia.clase).joinedload(Clase.aula))
            .filter(Asistencia.alumno_id == alumno_id, Clase.id.in_(clase_ids))
            .order_by(Clase.fecha)
            .all()
        )

        detalle = []
        asistencias_solas = []

        for asistencia, clase in asistencias:
            detalle.append(
                {
                    "id": clase.id,
                    "fecha": clase.fecha,
                    "clase_nombre": clase.tema,  # o clase.aula.nombre
                    "presente": asistencia.presente,
                    "justificado": asistencia.justificado,
                }
            )
            asistencias_solas.append(asistencia)

        resumen = calcular_asistencia(asistencias_solas, len(clase_ids))

        resultado.append(
            {
                "aula_id": aula.id,
                "materia": aula.nombre,
                "porcentaje_asistencia": resumen["porcentaje"],
                "asistencias": detalle,
            }
        )

    return resultado


def obtener_asistencias_por_alumno_y_aula(db: Session, alumno_id: int, aula_id: int):
    asistencias = (
        db.query(Asistencia)
        .join(Clase)
        .filter(Asistencia.alumno_id == alumno_id, Clase.aula_id == aula_id)
        .order_by(Clase.fecha)
        .all()
    )
    return asistencias


def obtener_asistencias_por_aula(db: Session, aula_id: int) -> List[AsistenciaPorAula]:
    clases = db.query(Clase).filter(Clase.aula_id == aula_id).all()
    clase_ids = [clase.id for clase in clases]

    if not clase_ids:
        return {"aula_id": aula_id, "resumen": [], "porcentaje_aula": 0}

    # Obtener todas las asistencias relacionadas a esas clases
    asistencias = (
        db.query(Asistencia, Alumno)
        .join(Clase, Asistencia.clase_id == Clase.id)
        .join(Alumno, Asistencia.alumno_id == Alumno.id)
        .filter(Clase.id.in_(clase_ids))
        .all()
    )

    # Agrupar asistencias por alumno
    resumen_por_alumno = {}
    total_clases = len(clase_ids)

    for asistencia, alumno in asistencias:
        if asistencia.presente not in (1, 2, 3):
            continue  # Saltear clases no válidas

        alumno_id = asistencia.alumno_id
        if alumno_id not in resumen_por_alumno:
            resumen_por_alumno[alumno_id] = {
                "alumno_id": alumno_id,
                "alumno_nombre": alumno.nombre,
                "presentes": 0,
                "ausentes": 0,
                "tardes": 0,
            }

        if asistencia.presente == 1:
            resumen_por_alumno[alumno_id]["presentes"] += 1
        elif asistencia.presente == 2:
            resumen_por_alumno[alumno_id]["ausentes"] += 1
        elif asistencia.presente == 3:
            resumen_por_alumno[alumno_id]["tardes"] += 1

    # Calcular porcentajes y armar salida
    salida = []
    total_porcentajes = 0

    for alumno_data in resumen_por_alumno.values():
        ausentes = alumno_data["ausentes"]
        tardes = alumno_data["tardes"]
        faltas_equivalentes = ausentes + (tardes // 3)

        porcentaje = (
            ((total_clases - faltas_equivalentes) / total_clases) * 100
            if total_clases > 0
            else 0
        )

        total_porcentajes += porcentaje

        salida.append(
            {
                "alumno_id": alumno_data["alumno_id"],
                "alumno_nombre": alumno_data["alumno_nombre"],
                "porcentaje_asistencia": round(porcentaje, 2),
            }
        )

    porcentaje_aula = (
        round(total_porcentajes / len(resumen_por_alumno), 2)
        if resumen_por_alumno
        else 0
    )

    return {
        "aula_id": aula_id,
        "asistencias": salida,
        "porcentaje_aula": porcentaje_aula,
    }


def calcular_asistencia(asistencias: List[Asistencia], total_clases: int) -> dict:
    presentes = ausentes = tardes = 0

    for asistencia in asistencias:
        if asistencia.presente == 1:
            presentes += 1
        elif asistencia.presente == 2:
            ausentes += 1
        elif asistencia.presente == 3:
            tardes += 1

    faltas_equivalentes = ausentes + (tardes / 3)
    porcentaje = (
        ((total_clases - faltas_equivalentes) / total_clases) * 100
        if total_clases > 0
        else 0
    )

    return {
        "presentes": presentes,
        "ausentes": ausentes,
        "tardes": tardes,
        "porcentaje": round(porcentaje, 2),
    }


def obtener_asistencias_por_clase(db: Session, clase_id: int) -> List[Dict[str, Any]]:
    # Obtener la clase
    clase = db.query(Clase).filter(Clase.id == clase_id).first()
    if not clase:
        raise ValueError("Clase no encontrada")

    # Obtener alumnos asignados al aula de esta clase
    aula = clase.aula
    alumnos = aula.alumnos  # debe estar definido como relación en el modelo Aula

    # Obtener asistencias ya registradas
    asistencias_registradas = (
        db.query(Asistencia).filter(Asistencia.clase_id == clase_id).all()
    )
    asistencias_map = {a.alumno_id: a for a in asistencias_registradas}

    # Construir lista final
    resultado = []
    for alumno in alumnos:
        asistencia = asistencias_map.get(alumno.id)
        resultado.append(
            {
                "alumno_id": alumno.id,
                "presente": asistencia.presente if asistencia else 2,
                "justificado": asistencia.justificado if asistencia else "no",
            }
        )

    return resultado
