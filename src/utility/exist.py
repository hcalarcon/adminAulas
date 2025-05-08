from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta


def existe(db: Session, model: DeclarativeMeta, **kwargs):
    return db.query(model).filter_by(**kwargs).first()
