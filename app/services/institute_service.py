from typing import Optional
from sqlalchemy.orm import Session
from ..schemas import InstituteCreate
from ..repositories.institute_repo import InstituteRepository


class InstituteService:
    @staticmethod
    def create_institute(db: Session, institute: InstituteCreate):
        return InstituteRepository.create(db, institute)

    @staticmethod
    def list_institutes(db: Session, search: Optional[str] = None):
        return InstituteRepository.get_all(db, search)

    @staticmethod
    def get_institute(db: Session, institute_id: int):
        return InstituteRepository.get_by_id(db, institute_id)

    @staticmethod
    def update_institute(db: Session, institute_id: int, data: dict):
        return InstituteRepository.update(db, institute_id, data)

    @staticmethod
    def delete_institute(db: Session, institute_id: int):
        return InstituteRepository.delete(db, institute_id)
