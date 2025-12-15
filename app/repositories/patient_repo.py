"""
Patient repository - Database access layer for Patient model
"""
from sqlalchemy.orm import Session
from ..models import Patient
from ..schemas import PatientCreate


class PatientRepository:
    """Repository for Patient database operations"""
    
    @staticmethod
    def create_patient(db: Session, patient: PatientCreate, user_id: int) -> Patient:
        """Create a new patient"""
        db_patient = Patient(
            id=user_id,
            full_name=patient.full_name,
            age=patient.age,
            gender=patient.gender,
            phone=patient.phone,
            blood_group_id=patient.blood_group_id,
            address=patient.address
        )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    
    @staticmethod
    def get_patient_by_id(db: Session, patient_id: int) -> Patient:
        """Get patient by ID"""
        return db.query(Patient).filter(Patient.id == patient_id).first()
    
    @staticmethod
    def get_all_patients(db: Session, skip: int = 0, limit: int = 100):
        """Get all patients with pagination"""
        return db.query(Patient).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_patient(db: Session, patient_id: int, update_data: dict) -> Patient:
        """Update patient"""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            for key, value in update_data.items():
                setattr(patient, key, value)
            db.commit()
            db.refresh(patient)
        return patient
    
    @staticmethod
    def delete_patient(db: Session, patient_id: int) -> bool:
        """Delete patient"""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            db.delete(patient)
            db.commit()
            return True
        return False
