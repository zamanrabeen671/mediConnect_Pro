"""
Patient repository - Database access layer for Patient model
"""
from sqlalchemy.orm import Session
from ..models import Patient, Appointment, Prescription
from datetime import date
from sqlalchemy.orm import joinedload
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

    @staticmethod
    def count_upcoming_appointments(db: Session, patient_id: int) -> int:
        """Count appointments for patient where appointment_date >= today"""
        today = date.today()
        return (
            db.query(Appointment)
            .filter(
                Appointment.patient_id == patient_id,
                Appointment.appointment_date >= today,
            )
            .count()
        )

    @staticmethod
    def count_visited_doctors(db: Session, patient_id: int) -> int:
        """Count distinct doctors for past appointments (appointment_date < today)"""
        today = date.today()
        return (
            db.query(Appointment.doctor_id)
            .filter(
                Appointment.patient_id == patient_id,
                Appointment.appointment_date < today,
            )
            .distinct()
            .count()
        )

    @staticmethod
    def count_active_prescriptions(db: Session, patient_id: int) -> int:
        """Count prescriptions for the patient"""
        return (
            db.query(Prescription)
            .filter(Prescription.patient_id == patient_id)
            .count()
        )

    @staticmethod
    def get_upcoming_appointments(db: Session, patient_id: int, limit: int = 10):
        """Return upcoming appointments for a patient, eager-loading doctor and schedule."""
        today = date.today()
        return (
            db.query(Appointment)
            .options(joinedload(Appointment.doctor), joinedload(Appointment.schedule))
            .filter(
                Appointment.patient_id == patient_id,
                Appointment.appointment_date >= today,
            )
            .order_by(Appointment.appointment_date, Appointment.appointment_time)
            .limit(limit)
            .all()
        )
