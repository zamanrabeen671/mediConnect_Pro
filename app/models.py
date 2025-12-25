from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Time,
    Date,
    Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    password = Column(String(255), nullable=True)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    doctor = relationship("Doctor", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)



class BloodGroup(Base):
    __tablename__ = "blood_groups"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(10), unique=True, nullable=False)

    patients = relationship("Patient", back_populates="blood_group")



class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    full_name = Column(String(120))
    specialization = Column(String(120))
    phone = Column(String(20))
    chamber = Column(String(256))
    institute = Column(String(256))
    bmdc_number = Column(String(20))
    experience = Column(String(20))
    qualifications = Column(Text)
    consultation_fee = Column(String(20))
    status = Column(String(20), default="pending")

    user = relationship("User", back_populates="doctor")
    schedules = relationship("DoctorSchedule", back_populates="doctor", cascade="all, delete")
    appointments = relationship("Appointment", back_populates="doctor")



class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    full_name = Column(String(120))
    age = Column(Integer)
    gender = Column(String(20))
    phone = Column(String(20))

    blood_group_id = Column(Integer, ForeignKey("blood_groups.id"))

    address = Column(String(256))
    serial_number = Column(Integer, unique=True)

    user = relationship("User", back_populates="patient")
    blood_group = relationship("BloodGroup", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")



class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    day_of_week = Column(String(50))
    start_time = Column(Time)
    end_time = Column(Time)
    max_patients = Column(Integer)
    duration_per_appointment = Column(Integer, default=30)

    doctor = relationship("Doctor", back_populates="schedules")
    appointments = relationship("Appointment", back_populates="schedule")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("doctor_schedules.id"), nullable=True)

    appointment_date = Column(Date)
    appointment_time = Column(Time, nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    schedule = relationship("DoctorSchedule", back_populates="appointments")
    prescription = relationship(
        "Prescription",
        back_populates="appointment",
        uselist=False,
        cascade="all, delete"
    )



class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True)
    appointment_id = Column(
        Integer,
        ForeignKey("appointments.id"),
        unique=True,
        nullable=False
    )
    patient_id = Column(Integer, ForeignKey("patients.id"))

    notes = Column(Text)
    document_path = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    appointment = relationship(
        "Appointment",
        back_populates="prescription"
    )

    medicines = relationship(
        "PrescriptionMedicine",
        back_populates="prescription",
        cascade="all, delete"
    )


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    strength = Column(String(50))        
    form = Column(String(50))            
    manufacturer = Column(String(150))

    prescription_medicines = relationship(
        "PrescriptionMedicine",
        back_populates="medicine",
        cascade="all, delete"
    )
    
class PrescriptionMedicine(Base):
    __tablename__ = "prescription_medicines"

    id = Column(Integer, primary_key=True, index=True)

    prescription_id = Column(
        Integer,
        ForeignKey("prescriptions.id"),
        nullable=False
    )
    medicine_id = Column(
        Integer,
        ForeignKey("medicines.id"),
        nullable=False
    )

    dosage = Column(String(50))           # 1+0+1
    duration = Column(String(50))         # 7 days
    instruction = Column(String(255))     # after meal, before meal

    prescription = relationship(
        "Prescription",
        back_populates="medicines"
    )
    medicine = relationship(
        "Medicine",
        back_populates="prescription_medicines"
    )
