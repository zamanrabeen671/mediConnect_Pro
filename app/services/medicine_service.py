"""
Medicine service - Business logic for medicine operations
"""
from sqlalchemy.orm import Session
from ..models import Medicine
from ..schemas import MedicineCreate, MedicineOut
from ..repositories.medicine_repo import MedicineRepository


class MedicineService:

    @staticmethod
    def create_medicine(db: Session, medicine: MedicineCreate) -> MedicineOut:
        new_med = MedicineRepository.create_medicine(db, medicine)
        return MedicineOut.from_orm(new_med)

    @staticmethod
    def get_medicine(db: Session, medicine_id: int) -> MedicineOut:
        med = MedicineRepository.get_medicine_by_id(db, medicine_id)
        if not med:
            return None
        return MedicineOut.from_orm(med)

    @staticmethod
    def list_medicines(db: Session, skip: int = 0, limit: int = 100):
        return MedicineRepository.get_all_medicines(db, skip, limit)

    @staticmethod
    def list_medicines_by_name(db: Session, name: str):
        return MedicineRepository.get_medicine_by_name(db, name)

    @staticmethod
    def update_medicine(db: Session, medicine_id: int, update_data: dict) -> MedicineOut:
        med = MedicineRepository.update_medicine(db, medicine_id, update_data)
        if not med:
            raise Exception("Medicine not found")
        return MedicineOut.from_orm(med)

    @staticmethod
    def delete_medicine(db: Session, medicine_id: int) -> bool:
        return MedicineRepository.delete_medicine(db, medicine_id)
