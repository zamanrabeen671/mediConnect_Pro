"""
Appointment repository - Database access layer for Appointment model
"""
from sqlalchemy.orm import Session, joinedload
from ..models import Appointment, Patient
from ..schemas import AppointmentCreate


class AppointmentRepository:
    """Repository for Appointment database operations"""
    
    @staticmethod
    def create_appointment(db: Session, appointment: AppointmentCreate) -> Appointment:
        db_appointment = Appointment(
            doctor_id=appointment.doctor_id,
            patient_id=appointment.patient_id,
            schedule_id=appointment.schedule_id,
            appointment_date=appointment.appointment_date
        )
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    
    @staticmethod
    def get_appointment_by_id(db: Session, appointment_id: int) -> Appointment:
        """Get appointment by ID"""
        return db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    @staticmethod
    def get_appointments_by_patient(db: Session, patient_id: int):
        """Get all appointments for a patient"""
        return db.query(Appointment).options(joinedload(Appointment.patient)).filter(Appointment.patient_id == patient_id).all()
    
    @staticmethod
    def get_appointments_by_doctor(db: Session, doctor_id: int):
        """Get all appointments for a doctor"""
        return (
        db.query(Appointment)
        .options(joinedload(Appointment.patient))  # load patient relationship
        .filter(Appointment.doctor_id == doctor_id)
        .all()
    )
    @staticmethod
    def get_patients_by_doctor(db: Session, doctor_id: int):
    
        patients = (
            db.query(Patient)
            .join(Appointment, Appointment.patient_id == Patient.id)
            .filter(Appointment.doctor_id == doctor_id)
            .distinct()
            .all()
        )
        return patients
    @staticmethod
    def get_all_appointments(db: Session, skip: int = 0, limit: int = 100):
        """Get all appointments with pagination"""
        return db.query(Appointment).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_appointment(db: Session, appointment_id: int, update_data: dict) -> Appointment:
        """Update appointment"""
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if appointment:
            for key, value in update_data.items():
                setattr(appointment, key, value)
            db.commit()
            db.refresh(appointment)
        return appointment
    
    @staticmethod
    def delete_appointment(db: Session, appointment_id: int) -> bool:
        """Delete appointment"""
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if appointment:
            db.delete(appointment)
            db.commit()
            return True
        return False
