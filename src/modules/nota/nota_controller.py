from sqlalchemy.orm import Session
from src.modules.nota.nota_model import NotaTarea
from src.modules.tarea.tarea_model import Tarea
from src.modules.evaluacion.model import CriterioEvaluacion
from src.modules.usuarios.user_model import Usuarios
from src.modules.clase.clase_model import Clase
from src.modules.asistencia.asistencia_model import Asistencia
from src.modules.nota.nota_schemas import (
    NotaTareaAsignacionMasiva,
    NotaTareaUpdate,
    NotaTareaCreate,
    NotaTareaEliminarMasiva,
    NotaTareaUpdateMasiva,
)
from fastapi import HTTPException
from collections import defaultdict


def asignar_tarea(db: Session, data: NotaTareaCreate):
    # Validar existencia de tarea y alumno
    tarea = db.query(Tarea).filter(Tarea.id == data.tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    alumno = db.query(Usuarios).filter(Usuarios.id == data.alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # Crear asignación
    asignacion = NotaTarea(**data.model_dump())
    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)
    return asignacion


def asignar_tarea_masiva(db: Session, data: NotaTareaAsignacionMasiva):
    # Validar que exista la tarea
    tarea = db.query(Tarea).filter(Tarea.id == data.tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    asignaciones = []
    for alumno_id in data.alumnos:
        alumno = db.query(Usuarios).filter(Usuarios.id == alumno_id).first()
        if not alumno:
            continue  # Opcional: podés lanzar error o solo omitir

        asignacion = NotaTarea(
            tarea_id=data.tarea_id,
            alumno_id=alumno_id,
            entregado=False,
            nota=None,
        )
        db.add(asignacion)
        asignaciones.append(asignacion)

    db.commit()
    for a in asignaciones:
        db.refresh(a)

    return asignaciones


def actualizar_nota_tarea(db: Session, nota_id: int, data: NotaTareaUpdate):
    nota = db.query(NotaTarea).filter(NotaTarea.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(nota, campo, valor)

    db.commit()
    db.refresh(nota)
    return nota


def eliminar_nota_tarea(db: Session, nota_id: int):
    nota = db.query(NotaTarea).filter(NotaTarea.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    db.delete(nota)
    db.commit()
    return {"msg": "Nota eliminada correctamente"}


def obtener_notas_por_alumno(db: Session, alumno_id: int):
    return db.query(NotaTarea).filter(NotaTarea.alumno_id == alumno_id).all()


def obtener_notas_por_tarea(db: Session, tarea_id: int):
    return db.query(NotaTarea).filter(NotaTarea.tarea_id == tarea_id).all()


def obtener_notas_por_alumno_y_aula(db: Session, alumno_id: int, aula_id: int):
    return (
        db.query(NotaTarea)
        .join(NotaTarea.tarea)
        .filter(NotaTarea.alumno_id == alumno_id, Tarea.aula_id == aula_id)
        .all()
    )


def obtener_notas_agrupadas_por_aula(db: Session, alumno_id: int):
    resultados = (
        db.query(NotaTarea, Tarea.aula_id)
        .join(Tarea, NotaTarea.tarea_id == Tarea.id)
        .filter(NotaTarea.alumno_id == alumno_id)
        .all()
    )

    notas_por_aula = defaultdict(list)
    for nota, aula_id in resultados:
        notas_por_aula[aula_id].append(nota)

    return dict(notas_por_aula)


def eliminar_notas_masivas(db: Session, data: NotaTareaEliminarMasiva):
    # Validar que exista la tarea
    tarea = db.query(Tarea).filter(Tarea.id == data.tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Eliminar las notas de los alumnos indicados
    db.query(NotaTarea).filter(
        NotaTarea.tarea_id == data.tarea_id, NotaTarea.alumno_id.in_(data.alumno_ids)
    ).delete(synchronize_session=False)

    db.commit()
    return {"detail": "Notas eliminadas correctamente"}


def actualizar_notas_masiva(db: Session, data: NotaTareaUpdateMasiva):
    tarea_id = data.tarea_id

    for nota_data in data.notas:
        nota = (
            db.query(NotaTarea)
            .filter_by(tarea_id=tarea_id, alumno_id=nota_data.alumno_id)
            .first()
        )

        if nota:
            if nota_data.nota is not None:
                nota.nota = nota_data.nota
            if nota_data.entregado is not None:
                nota.entregado = nota_data.entregado

    db.commit()
    return {"ok": True, "message": "Notas actualizadas correctamente"}


def calcular_nota_final(
    db: Session, alumno_id: int, aula_id: int, porcentaje_asistencia: float
):
    CORTE_ASISTENCIA = 80.0
    CORTE_NOTA_APROBACION = 7.0

    criterios = db.query(CriterioEvaluacion).filter_by(aula_id=aula_id).all()
    criterios_dict = {c.criterio: float(c.peso) for c in criterios}

    notas = (
        db.query(NotaTarea, Tarea)
        .join(Tarea, NotaTarea.tarea_id == Tarea.id)
        .filter(NotaTarea.alumno_id == alumno_id, Tarea.aula_id == aula_id)
        .all()
    )

    notas_agrupadas = {}
    for nota, tarea in notas:
        tipo = tarea.tipo
        criterio_key = "trabajos" if tipo in ["tt", "tp"] else tipo
        notas_agrupadas.setdefault(criterio_key, []).append(float(nota.nota))

    promedios = {}
    for criterio, notas_list in notas_agrupadas.items():
        promedios[criterio] = sum(notas_list) / len(notas_list)

    # Nota de asistencia: directa, sin elevar si pasa 90
    nota_asistencia = porcentaje_asistencia / 10  # ejemplo 91.5 → 9.15
    promedios["asistencia"] = nota_asistencia

    nota_sin_condiciones = 0.0
    detalles = {}

    for criterio, promedio in promedios.items():
        peso = criterios_dict.get(criterio, 0.0)
        contribucion = promedio * (peso / 100)
        detalles[criterio] = {
            "promedio": round(promedio, 2),
            "peso": round(peso, 2),
            "contribucion": round(contribucion, 2),
        }
        nota_sin_condiciones += contribucion

    # Validación de corte para aprobar:
    # Si alguno no cumple, bajamos nota final a valor menor a 7
    condiciones_fallidas = []

    if nota_asistencia < CORTE_ASISTENCIA / 10:  # 80% → 8.0 en nota escala 0-10
        condiciones_fallidas.append("asistencia")

    if promedios.get("trabajos", CORTE_NOTA_APROBACION + 1) < CORTE_NOTA_APROBACION:
        condiciones_fallidas.append("trabajos")

    if promedios.get("evaluacion", CORTE_NOTA_APROBACION + 1) < CORTE_NOTA_APROBACION:
        condiciones_fallidas.append("evaluacion")

    nota_final = nota_sin_condiciones
    if condiciones_fallidas:
        # Fijamos nota final como menor a 7 (puede ser el mínimo entre promedios fallidos o un fijo 6.9)
        nota_final = min(nota_sin_condiciones, 6.9)

    return {
        "nota_final": round(nota_final, 2),
        "nota_sin_condiciones": round(nota_sin_condiciones, 2),
        "detalles": detalles,
        "condiciones_fallidas": condiciones_fallidas,  # para debug o frontend
    }
