"""
Patient service - Business logic for patient operations
"""
from sqlalchemy.orm import Session
from ..models import Patient
from ..schemas import PatientCreate, PatientOut
from ..repositories.patient_repo import PatientRepository


class PatientService:
    """Service for patient-related business logic"""
    
    @staticmethod
    def create_patient(db: Session, patient: PatientCreate, user_id: int) -> PatientOut:
        """Create a new patient"""
        new_patient = PatientRepository.create_patient(db, patient, user_id)
        return PatientOut.from_orm(new_patient)
    
    @staticmethod
    def get_patient(db: Session, patient_id: int) -> PatientOut:
        """Get patient by ID"""
        patient = PatientRepository.get_patient_by_id(db, patient_id)
        if not patient:
            raise Exception("Patient not found")
        return PatientOut.from_orm(patient)
    
    @staticmethod
    def list_patients(db: Session, skip: int = 0, limit: int = 100):
        """List all patients"""
        return PatientRepository.get_all_patients(db, skip, limit)
    
    @staticmethod
    def update_patient(db: Session, patient_id: int, update_data: dict) -> PatientOut:
        """Update patient"""
        patient = PatientRepository.update_patient(db, patient_id, update_data)
        if not patient:
            raise Exception("Patient not found")
        return PatientOut.from_orm(patient)
    
    @staticmethod
    def delete_patient(db: Session, patient_id: int) -> bool:
        """Delete patient"""
        return PatientRepository.delete_patient(db, patient_id)
