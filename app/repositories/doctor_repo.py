"""
Doctor repository - Database access layer for Doctor model
"""
from sqlalchemy.orm import Session
from ..models import Doctor
from ..schemas import DoctorCreate


class DoctorRepository:
    
    @staticmethod
    def create_doctor(db: Session, doctor: DoctorCreate, user_id: int):
        db_doctor = Doctor(
            id=user_id,
            full_name=doctor.full_name,
            specialization=doctor.specialization,
            phone=doctor.phone,
            chamber=doctor.chamber,
            institute=doctor.institute,
            bmdc_number=doctor.bmdcNumber,
            experience=doctor.experience,
            qualifications=doctor.qualifications,
            consultation_fee=doctor.consultationFee,
            status="pending",
        )

        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor


    
    @staticmethod
    def get_doctor_by_id(db: Session, doctor_id: int) -> Doctor:
        return db.query(Doctor).filter(Doctor.id == doctor_id).first()
    
    @staticmethod
    def get_all_doctors(db: Session, skip: int = 0, limit: int = 100):
        """Get all doctors with pagination"""
        return db.query(Doctor).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_doctors_by_status(db: Session, status: str):
        """Get doctors by status"""
        return db.query(Doctor).filter(Doctor.status == status).all()
    
    @staticmethod
    def update_doctor(db: Session, doctor_id: int, update_data: dict) -> Doctor:
        """Update doctor"""
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            for key, value in update_data.items():
                setattr(doctor, key, value)
            db.commit()
            db.refresh(doctor)
        return doctor
    
    @staticmethod
    def delete_doctor(db: Session, doctor_id: int) -> bool:
        """Delete doctor"""
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            db.delete(doctor)
            db.commit()
            return True
        return False
