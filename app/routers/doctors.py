from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.models import Doctor

from ..database import get_db
from ..schemas import DoctorCreate, DoctorOut, ScheduleOut, AppointmentDoctorOut, DashboardStats
from ..services.doctor_service import DoctorService
from ..core.security import get_current_doctor

router = APIRouter(prefix="/api/v1/doctors", tags=["Doctors"])


@router.post("/", response_model=DoctorOut, status_code=status.HTTP_201_CREATED)
def create_doctor(
    doctor: DoctorCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.state.user_id

    return DoctorService.create_doctor(db, doctor, user_id=user_id)


@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return DoctorService.get_doctor(db, doctor_id)


@router.get("/", response_model=list[DoctorOut])
def list_doctors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return DoctorService.list_doctors(db, skip, limit)


@router.get("/status/{status}", response_model=list[DoctorOut])
def list_doctors_by_status(status: str, db: Session = Depends(get_db)):
    
    return DoctorService.list_doctors_by_status(db, status)


@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor(
    doctor_id: int,
    update_data: dict,
    db: Session = Depends(get_db)
):
    """Update doctor information"""
    return DoctorService.update_doctor(db, doctor_id, update_data)


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Delete doctor"""
    DoctorService.delete_doctor(db, doctor_id)
    return None


# Dashboard Endpoints
@router.get("/{doctor_id}/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(doctor_id: int, db: Session = Depends(get_db)):
    """Get dashboard statistics for a doctor (appointments, patients, reports)"""
    return DoctorService.get_dashboard_stats(db, doctor_id)


@router.get("/{doctor_id}/schedule", response_model=list[ScheduleOut])
def get_doctor_schedule(doctor_id: int, db: Session = Depends(get_db)):
    """Get doctor's schedule"""
    return DoctorService.get_doctor_schedule(db, doctor_id)


@router.get("/{doctor_id}/appointments/today", response_model=list[AppointmentDoctorOut])
def get_today_appointments(doctor_id: int, db: Session = Depends(get_db)):
    """Get all appointments for a doctor today"""
    return DoctorService.get_today_appointments(db, doctor_id)

