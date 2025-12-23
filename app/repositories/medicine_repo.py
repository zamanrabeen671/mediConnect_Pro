"""
Medicine repository - Database access layer for Medicine model
"""
from sqlalchemy.orm import Session
from ..models import Medicine
from ..schemas import MedicineCreate


class MedicineRepository:

    @staticmethod
    def create_medicine(db: Session, medicine: MedicineCreate) -> Medicine:
        db_med = Medicine(
            name=medicine.name,
            strength=medicine.strength,
            form=medicine.form,
            manufacturer=medicine.manufacturer,
        )
        db.add(db_med)
        db.commit()
        db.refresh(db_med)
        return db_med

    @staticmethod
    def get_medicine_by_id(db: Session, medicine_id: int) -> Medicine:
        return db.query(Medicine).filter(Medicine.id == medicine_id).first()

    @staticmethod
    def get_all_medicines(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Medicine).offset(skip).limit(limit).all()

    @staticmethod
    def get_medicine_by_name(db: Session, name: str):
        return db.query(Medicine).filter(Medicine.name == name).all()

    @staticmethod
    def update_medicine(db: Session, medicine_id: int, update_data: dict) -> Medicine:
        med = db.query(Medicine).filter(Medicine.id == medicine_id).first()
        if med:
            for key, value in update_data.items():
                setattr(med, key, value)
            db.commit()
            db.refresh(med)
        return med

    @staticmethod
    def delete_medicine(db: Session, medicine_id: int) -> bool:
        med = db.query(Medicine).filter(Medicine.id == medicine_id).first()
        if med:
            db.delete(med)
            db.commit()
            return True
        return False
