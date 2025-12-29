"""
Appointment routes
"""
from webbrowser import get
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import AppointmentCreate, AppointmentOut, AppointmentWithPatientCreate, AppointmentDoctorOut, PatientOut
from ..services.appointment_service import AppointmentService

router = APIRouter(prefix="/api/v1/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    
    return AppointmentService.create_appointment(db, appointment)


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Get appointment by ID"""
    return AppointmentService.get_appointment(db, appointment_id)

@router.post("/appointmentByPatient", response_model=AppointmentDoctorOut, status_code=status.HTTP_201_CREATED)
def create_appointment_with_patient(
    data: AppointmentWithPatientCreate,
    db: Session = Depends(get_db)
):
    """Create patient (if new) and appointment in one API call"""
    return AppointmentService.create_appointment_with_patient(db, data)
@router.get("/patient/{patient_id}", response_model=list[AppointmentOut])
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    return AppointmentService.get_patient_appointments(db, patient_id)


@router.get("/doctor/{doctor_id}", response_model=list[AppointmentDoctorOut])
def get_doctor_appointments(  request: Request,doctor_id: int, db: Session = Depends(get_db)):
    user_id = getattr(request.state, "user_id", None)
   
    return AppointmentService.get_doctor_appointments(db, user_id)


@router.get("/", response_model=list[AppointmentOut])
def list_appointments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all appointments"""
    return AppointmentService.list_appointments(db, skip, limit)

@router.get("/patients/doctor/{doctor_id}", response_model=list[PatientOut])
def get_patients_by_doctor(doctor_id: int, db: Session = Depends(get_db)):
    
    return AppointmentService.get_patients_by_doctor(db, doctor_id)

@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    appointment_id: int,
    update_data: dict,
    db: Session = Depends(get_db)
):
    """Update appointment"""
    return AppointmentService.update_appointment(db, appointment_id, update_data)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Delete appointment"""
    AppointmentService.delete_appointment(db, appointment_id)
    return None
