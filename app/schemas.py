from __future__ import annotations

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


# =========================
# SPECIALIZATION / INSTITUTE / QUALIFICATION
# =========================
class SpecializationCreate(BaseModel):
    name: str


class SpecializationOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class InstituteCreate(BaseModel):
    name: str
    address: Optional[str] = None


class InstituteOut(BaseModel):
    id: int
    name: str
    address: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class QualificationCreate(BaseModel):
    name: str


class QualificationOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class DoctorCreate(BaseModel):
    full_name: str
    phone: str
    chamber: Optional[str] = None
    bmdc_number: Optional[str] = None
    experience: Optional[str] = None
    consultation_fee: Optional[str] = None
    # Accept lists of ids for relationships (optional)
    specialization_ids: Optional[list[int]] = None
    institute_ids: Optional[list[int]] = None
    qualification_ids: Optional[list[int]] = None
    qualification_names: Optional[list[str]] = None


class DoctorOut(BaseModel):
    id: int
    full_name: str
    phone: Optional[str] = None
    chamber: Optional[str] = None
    bmdc_number: Optional[str] = None
    experience: Optional[str] = None
    consultation_fee: Optional[str] = None
    status: str
    specializations: Optional[list[SpecializationOut]] = None
    institutes: Optional[list[InstituteOut]] = None
    qualifications: Optional[list[QualificationOut]] = None

    model_config = {
        "from_attributes": True
    }
# =========================
# PATIENT
# =========================
class PatientCreate(BaseModel):
    full_name: str
    age: int
    email: Optional[str] = None
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
    appointment_time: time


class AppointmentOut(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    schedule_id: Optional[int]
    appointment_date: date
    appointment_time: Optional[time] = None
    status: str

    model_config = {
        "from_attributes": True  
    }


class AppointmentWithDoctorOut(AppointmentOut):
    doctor: Optional[DoctorOut] = None

    model_config = {
        "from_attributes": True
    }


class UpcomingAppointmentOut(BaseModel):
    id: int
    appointment_date: date
    appointment_time: Optional[time] = None
    status: str
    doctor: Optional[DoctorOut] = None

    model_config = {
        "from_attributes": True
    }

class AppointmentDoctorOut(BaseModel):
    id: int
    doctor_id: int
    patient: PatientOut 
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
    appointment_time: Optional[time] = None
# =========================
# PRESCRIPTION
# =========================
class PrescriptionCreate(BaseModel):
    appointment_id: int
    patient_id: int
    notes: str
    medicines: Optional[list["PrescriptionMedicineCreate"]] = None


class MedicineCreate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    strength: Optional[str] = None
    form: Optional[str] = None
    manufacturer: Optional[str] = None


class MedicineOut(BaseModel):
    id: int
    name: str
    strength: Optional[str] = None
    form: Optional[str] = None
    manufacturer: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class PrescriptionMedicineCreate(BaseModel):
    medicine_id: Optional[int] = None
    medicine: Optional[MedicineCreate] = None
    dosage: Optional[str] = None
    duration: Optional[str] = None
    instruction: Optional[str] = None


class PrescriptionMedicineOut(BaseModel):
    id: int
    medicine: MedicineOut
    dosage: Optional[str] = None
    duration: Optional[str] = None
    instruction: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class PrescriptionOut(PrescriptionCreate):
    id: int
    document_path: Optional[str] = None
    medicines: Optional[list[PrescriptionMedicineOut]] = None

    model_config = {
        "from_attributes": True
    }


class PrescriptionWithDoctorOut(PrescriptionOut):
    # include appointment (which can include doctor) for richer response
    appointment: Optional[AppointmentWithDoctorOut] = None
    model_config = {
        "from_attributes": True
    }


# =========================
# DOCTOR DASHBOARD
# =========================
class DashboardStats(BaseModel):
    today_appointments: int
    total_patients: int
    pending_reports: int
    
    model_config = {
        "from_attributes": True
    }

