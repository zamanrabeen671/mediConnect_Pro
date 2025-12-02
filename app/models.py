from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Time, Date, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    full_name = Column(String(120))
    specialization = Column(String(120))
    phone = Column(String(20))
    chamber = Column(String(256))
    status = Column(String(20), default="pending")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    full_name = Column(String(120))
    age = Column(Integer)
    gender = Column(String(20))
    phone = Column(String(20))
    blood_group = Column(String(20))
    address = Column(String(256))


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    day_of_week = Column(String(20))
    start_time = Column(Time)
    end_time = Column(Time)
    max_patients = Column(Integer)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("doctor_schedules.id"), nullable=False)
    appointment_date = Column(Date)
    status = Column(String(20), default="pending")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    notes = Column(Text)
    document_path = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
