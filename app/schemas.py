from pydantic import BaseModel
from datetime import time, date
from typing import Optional


# =========================
# USERS
# =========================
class UserCreate(BaseModel):
    email: str
    password: str
    role: str


class UserOut(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        orm_mode = True


# =========================
# BLOOD GROUP
# =========================
class BloodGroupCreate(BaseModel):
    group_name: str


class BloodGroupOut(BaseModel):
    id: int
    group_name: str

    class Config:
        orm_mode = True


# =========================
# DOCTOR
# =========================
class DoctorCreate(BaseModel):
    full_name: str
    specialization: str
    phone: str
    chamber: str


class DoctorOut(DoctorCreate):
    id: int
    status: str

    class Config:
        orm_mode = True


# =========================
# PATIENT
# =========================
class PatientCreate(BaseModel):
    full_name: str
    age: int
    gender: str
    phone: str
    blood_group_id: int    # FK instead of text
    address: str


class PatientOut(BaseModel):
    id: int
    full_name: str
    age: int
    gender: str
    phone: str
    address: str

    blood_group: BloodGroupOut   # nested response

    class Config:
        orm_mode = True


# =========================
# SCHEDULE
# =========================
class ScheduleCreate(BaseModel):
    doctor_id: int
    day_of_week: str
    start_time: time
    end_time: time
    max_patients: int


class ScheduleOut(ScheduleCreate):
    id: int

    class Config:
        orm_mode = True


# =========================
# APPOINTMENT
# =========================
class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    schedule_id: int
    appointment_date: date


class AppointmentOut(AppointmentCreate):
    id: int
    status: str

    class Config:
        orm_mode = True


# =========================
# PRESCRIPTION
# =========================
class PrescriptionCreate(BaseModel):
    appointment_id: int
    patient_id: int
    notes: str


class PrescriptionOut(PrescriptionCreate):
    id: int
    document_path: Optional[str] = None

    class Config:
        orm_mode = True
