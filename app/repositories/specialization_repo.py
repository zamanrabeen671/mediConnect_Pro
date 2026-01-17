from typing import Optional
from sqlalchemy.orm import Session
from ..models import Specialization
from ..schemas import SpecializationCreate


class SpecializationRepository:
    @staticmethod
    def create(db: Session, specialization: SpecializationCreate) -> Specialization:
        new = Specialization(name=specialization.name)
        db.add(new)
        db.commit()
        db.refresh(new)
        return new

    @staticmethod
    def get_all(db: Session, search: Optional[str] = None):
        q = db.query(Specialization)
        if search:
            q = q.filter(Specialization.name.ilike(f"%{search}%"))
        return q.all()

    @staticmethod
    def get_by_id(db: Session, specialization_id: int):
        return db.query(Specialization).filter(Specialization.id == specialization_id).first()

    @staticmethod
    def update(db: Session, specialization_id: int, data: dict):
        obj = SpecializationRepository.get_by_id(db, specialization_id)
        if not obj:
            return None
        if "name" in data:
            obj.name = data["name"]
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, specialization_id: int):
        obj = SpecializationRepository.get_by_id(db, specialization_id)
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return True
