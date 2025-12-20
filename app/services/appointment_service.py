"""
Appointment service - Business logic for appointment operations
"""
from sqlalchemy.orm import Session
from ..models import Appointment, Patient, User
from ..schemas import AppointmentCreate, AppointmentOut, AppointmentWithPatientCreate
from ..repositories.appointment_repo import AppointmentRepository
import random
import uuid

class AppointmentService:
    
    @staticmethod
    def create_appointment(db: Session, appointment: AppointmentCreate) -> AppointmentOut:
        new_appointment = AppointmentRepository.create_appointment(db, appointment)
        return AppointmentOut.from_orm(new_appointment)
    
    @staticmethod
    def create_appointment_with_patient(db: Session, data: AppointmentWithPatientCreate) -> AppointmentOut:
        

        def generate_8digit_id():
            return random.randint(10000000, 99999999)

        serial_number = generate_8digit_id()
        temp_email = f"patient_{uuid.uuid4().hex[:8]}@example.com"
        new_user = User(
        email=temp_email,
        role="patient",
        
        # no password
        )
        db.add(new_user)
        db.flush()
        new_patient = Patient(
            id=new_user.id,
            full_name=data.patient.full_name,
            age=data.patient.age,
            gender=data.patient.gender,
            phone=data.patient.phone,
            blood_group_id=data.patient.blood_group_id,
            address=data.patient.address,
            serial_number=serial_number,
        )
        db.add(new_patient)
        db.flush()  # flush to get new_patient.id without committing

        # 2. Create appointment
        new_appointment = Appointment(
            doctor_id=data.doctor_id,
            patient_id=new_patient.id,
            schedule_id=data.schedule_id,
            appointment_date=data.appointment_date
        )
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

        return AppointmentOut.from_orm(new_appointment)
    
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
    def delete_appointment(db: Session, appointment_id: int) -> bool:
        """Delete appointment"""
        return AppointmentRepository.delete_appointment(db, appointment_id)
