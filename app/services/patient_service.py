"""
Patient service - Business logic for patient operations
"""
from sqlalchemy.orm import Session
from ..models import Patient
from ..repositories.patient_repo import PatientRepository
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

    @staticmethod
    def get_dashboard_stats(db: Session, patient_id: int) -> dict:
        """Return dashboard counts for a patient:
        - upcoming appointments (appointment_date >= today)
        - visited doctors (distinct doctors with past appointments)
        - active prescriptions (count of prescriptions)
        """
        upcoming_appointments = PatientRepository.count_upcoming_appointments(db, patient_id)
        visited_doctors = PatientRepository.count_visited_doctors(db, patient_id)
        active_prescriptions = PatientRepository.count_active_prescriptions(db, patient_id)

        return {
            "upcoming_appointments": upcoming_appointments,
            "visited_doctors": visited_doctors,
            "active_prescriptions": active_prescriptions,
        }

    @staticmethod
    def list_upcoming_appointments(db: Session, patient_id: int, limit: int = 10):
        """Return list of upcoming appointments for a patient."""
        appointments = PatientRepository.get_upcoming_appointments(db, patient_id, limit)
        return appointments

    @staticmethod
    def search_by_phone(db: Session, phone: str):
        """Search patients by phone and return list of PatientOut."""
        patients = PatientRepository.search_patients_by_phone(db, phone)
        return [PatientOut.from_orm(p) for p in patients]
