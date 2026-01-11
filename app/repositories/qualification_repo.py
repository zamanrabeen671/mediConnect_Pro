from sqlalchemy.orm import Session
from ..models import Qualification
from ..schemas import QualificationCreate


class QualificationRepository:
    @staticmethod
    def create(db: Session, qualification: QualificationCreate) -> Qualification:
        new = Qualification(name=qualification.name)
        db.add(new)
        db.commit()
        db.refresh(new)
        return new

    @staticmethod
    def get_all(db: Session, search: str | None = None):
        q = db.query(Qualification)
        if search:
            q = q.filter(Qualification.name.ilike(f"%{search}%"))
        return q.all()

    @staticmethod
    def get_by_id(db: Session, qualification_id: int):
        return db.query(Qualification).filter(Qualification.id == qualification_id).first()

    @staticmethod
    def update(db: Session, qualification_id: int, data: dict):
        obj = QualificationRepository.get_by_id(db, qualification_id)
        if not obj:
            return None
        if "name" in data:
            obj.name = data["name"]
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, qualification_id: int):
        obj = QualificationRepository.get_by_id(db, qualification_id)
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return True
