# app/services/blood_group_service.py
from sqlalchemy.orm import Session
from ..schemas import BloodGroupCreate
from ..repositories.blood_group import BloodGroupRepository

class BloodGroupService:
    @staticmethod
    def create_blood_group(db: Session, blood_group: BloodGroupCreate):
        return BloodGroupRepository.create(db, blood_group)

    @staticmethod
    def get_all_blood_groups(db: Session):
        return BloodGroupRepository.get_all(db)
