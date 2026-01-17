from typing import Optional
from sqlalchemy.orm import Session
from ..schemas import SpecializationCreate
from ..repositories.specialization_repo import SpecializationRepository


class SpecializationService:
    @staticmethod
    def create_specialization(db: Session, specialization: SpecializationCreate):
        return SpecializationRepository.create(db, specialization)

    @staticmethod
    def list_specializations(db: Session, search: Optional[str] = None):
        return SpecializationRepository.get_all(db, search)

    @staticmethod
    def get_specialization(db: Session, specialization_id: int):
        return SpecializationRepository.get_by_id(db, specialization_id)

    @staticmethod
    def update_specialization(db: Session, specialization_id: int, data: dict):
        return SpecializationRepository.update(db, specialization_id, data)

    @staticmethod
    def delete_specialization(db: Session, specialization_id: int):
        return SpecializationRepository.delete(db, specialization_id)
