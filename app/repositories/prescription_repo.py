"""
Prescription repository - Database access layer for Prescription model
"""
from sqlalchemy.orm import Session
from ..models import Prescription
from ..schemas import PrescriptionCreate


class PrescriptionRepository:
    """Repository for Prescription database operations"""
    
    @staticmethod
    def create_prescription(db: Session, prescription: PrescriptionCreate) -> Prescription:
        """Create a new prescription"""
        db_prescription = Prescription(
            appointment_id=prescription.appointment_id,
            patient_id=prescription.patient_id,
            notes=prescription.notes
        )
        db.add(db_prescription)
        db.commit()
        db.refresh(db_prescription)
        return db_prescription
    
    @staticmethod
    def get_prescription_by_id(db: Session, prescription_id: int) -> Prescription:
        """Get prescription by ID"""
        return db.query(Prescription).filter(Prescription.id == prescription_id).first()
    
    @staticmethod
    def get_prescription_by_appointment(db: Session, appointment_id: int) -> Prescription:
        """Get prescription by appointment ID"""
        return db.query(Prescription).filter(Prescription.appointment_id == appointment_id).first()
    
    @staticmethod
    def get_prescriptions_by_patient(db: Session, patient_id: int):
        """Get all prescriptions for a patient"""
        return db.query(Prescription).filter(Prescription.patient_id == patient_id).all()
    
    @staticmethod
    def get_all_prescriptions(db: Session, skip: int = 0, limit: int = 100):
        """Get all prescriptions with pagination"""
        return db.query(Prescription).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_prescription(db: Session, prescription_id: int, update_data: dict) -> Prescription:
        """Update prescription"""
        prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
        if prescription:
            for key, value in update_data.items():
                setattr(prescription, key, value)
            db.commit()
            db.refresh(prescription)
        return prescription
    
    @staticmethod
    def delete_prescription(db: Session, prescription_id: int) -> bool:
        """Delete prescription"""
        prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
        if prescription:
            db.delete(prescription)
            db.commit()
            return True
        return False
