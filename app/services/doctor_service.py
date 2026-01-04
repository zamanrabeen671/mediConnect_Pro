from sqlalchemy.orm import Session
from ..models import Doctor
from ..schemas import DoctorCreate, DoctorOut
from ..repositories.doctor_repo import DoctorRepository
from ..repositories.appointment_repo import AppointmentRepository
from ..repositories.schedule_repo import ScheduleRepository


class DoctorService:
    
    @staticmethod
    def create_doctor(db: Session, doctor: DoctorCreate, user_id: int) -> DoctorOut:
        new_doctor = DoctorRepository.create_doctor(db, doctor, user_id)
        return new_doctor                       
    
    @staticmethod
    def get_doctor(db: Session, doctor_id: int) -> DoctorOut:
        """Get doctor by ID"""
        doctor = DoctorRepository.get_doctor_by_id(db, doctor_id)
        if not doctor:
            # raise Exception("Doctor not found")
            return None
        return doctor
    
    @staticmethod
    def list_doctors(db: Session, skip: int = 0, limit: int = 100):
        return DoctorRepository.get_all_doctors(db, skip, limit)
    
    @staticmethod
    def list_doctors_by_status(db: Session, status: str):
        """List doctors by status"""
        return DoctorRepository.get_doctors_by_status(db, status)
    
    @staticmethod
    def update_doctor(db: Session, doctor_id: int, update_data: dict) -> DoctorOut:
        doctor = DoctorRepository.update_doctor(db, doctor_id, update_data)
        if not doctor:
            raise Exception("Doctor not found")
        return doctor
    
    @staticmethod
    def delete_doctor(db: Session, doctor_id: int) -> bool:
        """Delete doctor"""
        return DoctorRepository.delete_doctor(db, doctor_id)

    @staticmethod
    def get_dashboard_stats(db: Session, doctor_id: int) -> dict:
        """Get dashboard statistics for a doctor"""
        today_appointments = AppointmentRepository.get_appointment_count_today(db, doctor_id)
        total_patients = DoctorRepository.get_patient_count(db, doctor_id)
        pending_reports = AppointmentRepository.get_pending_reports_count(db, doctor_id)
        
        return {
            "today_appointments": today_appointments,
            "total_patients": total_patients,
            "pending_reports": pending_reports
        }
    
    @staticmethod
    def get_doctor_schedule(db: Session, doctor_id: int):
        """Get doctor's schedule"""
        return ScheduleRepository.get_schedules_by_doctor(db, doctor_id)
    
    @staticmethod
    def get_today_appointments(db: Session, doctor_id: int):
        """Get all appointments for a doctor today"""
        return AppointmentRepository.get_today_appointments_by_doctor(db, doctor_id)
