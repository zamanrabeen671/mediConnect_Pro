"""
Prescription service - Business logic for prescription operations
"""
from sqlalchemy.orm import Session
from ..models import Prescription
from ..schemas import PrescriptionCreate, PrescriptionOut
from ..repositories.prescription_repo import PrescriptionRepository
from ..repositories.appointment_repo import AppointmentRepository
from ..exceptions.http_exceptions import ResourceNotFoundException, PermissionDeniedException


class PrescriptionService:
    """Service for prescription-related business logic"""
    
    @staticmethod
    def create_prescription(db: Session, prescription: PrescriptionCreate, current_doctor=None) -> PrescriptionOut:
        
        appointment = AppointmentRepository.get_appointment_by_id(db, prescription.appointment_id)
        if not appointment:
            raise ResourceNotFoundException("Appointment not found")

        if current_doctor and appointment.doctor_id != current_doctor.id:
            raise PermissionDeniedException("You are not allowed to create a prescription for this appointment")
        updateAppointment = AppointmentRepository.update_appointment(
            db,
            appointment.id,
            {"status": "completed"}
        )
        new_prescription = PrescriptionRepository.create_prescription(db, prescription)
        return PrescriptionOut.from_orm(new_prescription)
    
    @staticmethod
    def get_prescription(db: Session, prescription_id: int) -> PrescriptionOut:
       
        prescription = PrescriptionRepository.get_prescription_by_id(db, prescription_id)
        if not prescription:
            raise Exception("Prescription not found")
        return PrescriptionOut.from_orm(prescription)
    
    @staticmethod
    def get_prescription_by_appointment(db: Session, appointment_id: int) -> PrescriptionOut:
        """Get prescription by appointment ID"""
        prescription = PrescriptionRepository.get_prescription_by_appointment(db, appointment_id)
        if not prescription:
            raise Exception("Prescription not found")
        return PrescriptionOut.from_orm(prescription)
    
    @staticmethod
    def get_patient_prescriptions(db: Session, patient_id: int):
        """Get all prescriptions for a patient"""
        return PrescriptionRepository.get_prescriptions_by_patient(db, patient_id)
    
    @staticmethod
    def list_prescriptions(db: Session, skip: int = 0, limit: int = 100):
        """List all prescriptions"""
        return PrescriptionRepository.get_all_prescriptions(db, skip, limit)
    
    @staticmethod
    def update_prescription(db: Session, prescription_id: int, update_data: dict) -> PrescriptionOut:
        """Update prescription"""
        prescription = PrescriptionRepository.update_prescription(db, prescription_id, update_data)
        if not prescription:
            raise Exception("Prescription not found")
        return PrescriptionOut.from_orm(prescription)
    
    @staticmethod
    def delete_prescription(db: Session, prescription_id: int) -> bool:
        """Delete prescription"""
        return PrescriptionRepository.delete_prescription(db, prescription_id)
