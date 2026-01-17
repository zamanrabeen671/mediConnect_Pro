from typing import Optional
from sqlalchemy.orm import Session
from ..models import Institute
from ..schemas import InstituteCreate


class InstituteRepository:
    @staticmethod
    def create(db: Session, institute: InstituteCreate) -> Institute:
        new = Institute(name=institute.name, address=institute.address)
        db.add(new)
        db.commit()
        db.refresh(new)
        return new

    @staticmethod
    def get_all(db: Session, search:Optional[str] = None):
        q = db.query(Institute)
        if search:
            q = q.filter(Institute.name.ilike(f"%{search}%"))
        return q.all()

    @staticmethod
    def get_by_id(db: Session, institute_id: int):
        return db.query(Institute).filter(Institute.id == institute_id).first()

    @staticmethod
    def update(db: Session, institute_id: int, data: dict):
        obj = InstituteRepository.get_by_id(db, institute_id)
        if not obj:
            return None
        if "name" in data:
            obj.name = data["name"]
        if "address" in data:
            obj.address = data["address"]
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, institute_id: int):
        obj = InstituteRepository.get_by_id(db, institute_id)
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return True
