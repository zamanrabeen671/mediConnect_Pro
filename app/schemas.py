from pydantic import BaseModel, Field
from datetime import time, date
from typing import Optional



class LoginRequest(BaseModel):
    email: str
    password: str
    
class UserCreate(BaseModel):
    email: str
    password: str
    role: str


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    status: Optional[str] = None
    model_config = {
        "from_attributes": True
    }


# =========================
# BLOOD GROUP
# =========================
class BloodGroupCreate(BaseModel):
    group_name: str


class BloodGroupOut(BaseModel):
    id: int
    group_name: str

    model_config = {
        "from_attributes": True
    }


class DoctorCreate(BaseModel):
    full_name: str
    specialization: str
    phone: str
    chamber: str
    institute: str
    bmdcNumber: str
    experience: str
    qualifications: str
    consultationFee: str


class DoctorOut(BaseModel):
    id: int
    full_name: str
    specialization: str
    phone: str
    chamber: str
    institute: str
    bmdcNumber: str = Field(..., alias="bmdc_number")
    experience: str
    qualifications: str
    consultationFee: str = Field(..., alias="consultation_fee")
    status: str

    model_config = {
        "from_attributes": True
    }
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

    blood_group: Optional[BloodGroupOut] = None   # nested response

    model_config = {
        "from_attributes": True 
    }



class ScheduleCreate(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time
    max_patients: int
    duration_per_appointment: Optional[int] = 30

class ScheduleCreateInternal(ScheduleCreate):
    doctor_id: int
    
class ScheduleOut(ScheduleCreate):
    id: int

    model_config = {
        "from_attributes": True 
    }



class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    schedule_id: Optional[int] = None
    appointment_date: date


class AppointmentOut(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    schedule_id: Optional[int]
    appointment_date: date
    appointment_time: time
    status: str

    model_config = {
        "from_attributes": True  
    }

class AppointmentDoctorOut(BaseModel):
    id: int
    doctor_id: int
    patient: PatientOut  # nested patient schema
    schedule_id: Optional[int]
    appointment_date: date
    appointment_time: Optional[time]
    status: str

    model_config = {
        "from_attributes": True
    }
class AppointmentWithPatientCreate(BaseModel):
    patient: PatientCreate
    doctor_id: int
    schedule_id: Optional[int] = None
    appointment_date: date

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
