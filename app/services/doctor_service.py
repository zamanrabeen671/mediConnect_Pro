"""
Doctor service - Business logic for doctor operations
"""
from sqlalchemy.orm import Session
from ..models import Doctor
from ..schemas import DoctorCreate, DoctorOut
from ..repositories.doctor_repo import DoctorRepository


class DoctorService:
    """Service for doctor-related business logic"""
    
    @staticmethod
    def create_doctor(db: Session, doctor: DoctorCreate, user_id: int) -> DoctorOut:
        """Create a new doctor"""
        new_doctor = DoctorRepository.create_doctor(db, doctor, user_id)
        return DoctorOut.from_orm(new_doctor)
    
    @staticmethod
    def get_doctor(db: Session, doctor_id: int) -> DoctorOut:
        """Get doctor by ID"""
        doctor = DoctorRepository.get_doctor_by_id(db, doctor_id)
        if not doctor:
            raise Exception("Doctor not found")
        return DoctorOut.from_orm(doctor)
    
    @staticmethod
    def list_doctors(db: Session, skip: int = 0, limit: int = 100):
        """List all doctors"""
        return DoctorRepository.get_all_doctors(db, skip, limit)
    
    @staticmethod
    def list_doctors_by_status(db: Session, status: str):
        """List doctors by status"""
        return DoctorRepository.get_doctors_by_status(db, status)
    
    @staticmethod
    def update_doctor(db: Session, doctor_id: int, update_data: dict) -> DoctorOut:
        """Update doctor"""
        doctor = DoctorRepository.update_doctor(db, doctor_id, update_data)
        if not doctor:
            raise Exception("Doctor not found")
        return DoctorOut.from_orm(doctor)
    
    @staticmethod
    def delete_doctor(db: Session, doctor_id: int) -> bool:
        """Delete doctor"""
        return DoctorRepository.delete_doctor(db, doctor_id)
