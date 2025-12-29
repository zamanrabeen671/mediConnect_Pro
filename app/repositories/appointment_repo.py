"""
Appointment repository - Database access layer for Appointment model
"""
from sqlalchemy.orm import Session, joinedload
from ..models import Appointment, Patient, User
from ..schemas import AppointmentCreate, AppointmentWithPatientCreate
import random
import uuid
from ..utils import hash_password, generate_temp_password

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
    def create_appointment_with_patient(
        db: Session,
        data: AppointmentWithPatientCreate
    ) -> Appointment:
        


        def generate_8digit_id():
            return random.randint(10000000, 99999999)

        serial_number = generate_8digit_id()
        while db.query(Patient).filter(Patient.serial_number == serial_number).first():
            serial_number = generate_8digit_id()

        temp_password = generate_temp_password()
        hashed_password = hash_password(temp_password)

        # use provided email or fallback
        email = data.patient.email

        # 1️⃣ Create user
        new_user = User(
            email=email,
            password=hashed_password,
            role="patient",
        )
        db.add(new_user)
        db.flush()

        # 2️⃣ Create patient
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
        db.flush()

        # 3️⃣ Create appointment
        new_appointment = Appointment(
            doctor_id=data.doctor_id,
            patient_id=new_patient.id,
            schedule_id=data.schedule_id,
            appointment_date=data.appointment_date,
            appointment_time=data.appointment_time
        )
        db.add(new_appointment)

        db.commit()
        db.refresh(new_appointment)

        # attach temp password for service layer usage (not stored)
        new_appointment._temp_password = temp_password
        new_appointment._email = email

        return new_appointment
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
