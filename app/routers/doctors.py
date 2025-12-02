from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Doctor
from ..schemas import DoctorCreate, DoctorOut

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/", response_model=DoctorOut)
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    doctor = Doctor(**data.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()
