from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models import Doctor

from ..database import get_db
from ..schemas import DoctorCreate, DoctorOut
from ..services.doctor_service import DoctorService
from ..core.security import get_current_doctor

router = APIRouter(prefix="/api/v1/doctors", tags=["Doctors"])


@router.post("/", response_model=DoctorOut, status_code=status.HTTP_201_CREATED)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
   
    return DoctorService.create_doctor(db, doctor, user_id=1)


@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Get doctor by ID"""
    return DoctorService.get_doctor(db, doctor_id)


@router.get("/", response_model=list[DoctorOut])
def list_doctors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all doctors"""
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
@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()
