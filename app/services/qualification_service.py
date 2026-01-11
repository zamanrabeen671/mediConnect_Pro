from sqlalchemy.orm import Session
from ..schemas import QualificationCreate
from ..repositories.qualification_repo import QualificationRepository


class QualificationService:
    @staticmethod
    def create_qualification(db: Session, qualification: QualificationCreate):
        return QualificationRepository.create(db, qualification)

    @staticmethod
    def list_qualifications(db: Session, search: str | None = None):
        return QualificationRepository.get_all(db, search)

    @staticmethod
    def get_qualification(db: Session, qualification_id: int):
        return QualificationRepository.get_by_id(db, qualification_id)

    @staticmethod
    def update_qualification(db: Session, qualification_id: int, data: dict):
        return QualificationRepository.update(db, qualification_id, data)

    @staticmethod
    def delete_qualification(db: Session, qualification_id: int):
        return QualificationRepository.delete(db, qualification_id)
