"""
Appointment service - Business logic for appointment operations
"""
from sqlalchemy.orm import Session
from ..schemas import AppointmentCreate, AppointmentOut, AppointmentWithPatientCreate,AppointmentDoctorOut
from ..repositories.appointment_repo import AppointmentRepository
from ..utils import send_patient_welcome_email
class AppointmentService:
    
    @staticmethod
    def create_appointment(db: Session, appointment: AppointmentCreate) -> AppointmentOut:
        new_appointment = AppointmentRepository.create_appointment(db, appointment)
        return AppointmentOut.from_orm(new_appointment)
    
    @staticmethod
    def create_appointment_with_patient(db: Session, data: AppointmentWithPatientCreate) -> AppointmentDoctorOut:
        appointment = AppointmentRepository.create_appointment_with_patient(db, data)
        if hasattr(appointment, "_email"):
            send_patient_welcome_email(
                appointment._email,
                appointment._temp_password
            )

        return AppointmentDoctorOut.from_orm(appointment)
    
    @staticmethod
    def get_appointment(db: Session, appointment_id: int) -> AppointmentOut:
        """Get appointment by ID"""
        appointment = AppointmentRepository.get_appointment_by_id(db, appointment_id)
        if not appointment:
            raise Exception("Appointment not found")
        return AppointmentOut.from_orm(appointment)
    
    @staticmethod
    def get_patient_appointments(db: Session, patient_id: int):
        """Get all appointments for a patient"""
        return AppointmentRepository.get_appointments_by_patient(db, patient_id)
    
    @staticmethod
    def get_doctor_appointments(db: Session, doctor_id: int):
        """Get all appointments for a doctor"""
        return AppointmentRepository.get_appointments_by_doctor(db, doctor_id)
    
    @staticmethod
    def list_appointments(db: Session, skip: int = 0, limit: int = 100):
        """List all appointments"""
        return AppointmentRepository.get_all_appointments(db, skip, limit)
    
    @staticmethod
    def update_appointment(db: Session, appointment_id: int, update_data: dict) -> AppointmentOut:
        """Update appointment"""
        appointment = AppointmentRepository.update_appointment(db, appointment_id, update_data)
        if not appointment:
            raise Exception("Appointment not found")
        return AppointmentOut.from_orm(appointment)
    @staticmethod
    def get_patients_by_doctor(db: Session, doctor_id: int):
        """Get all patients for a doctor"""
        return AppointmentRepository.get_patients_by_doctor(db, doctor_id)
    @staticmethod
    def delete_appointment(db: Session, appointment_id: int) -> bool:
        """Delete appointment"""
        return AppointmentRepository.delete_appointment(db, appointment_id)
