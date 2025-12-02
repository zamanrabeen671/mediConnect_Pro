from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Prescription
from ..schemas import PrescriptionCreate, PrescriptionOut

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


@router.post("/", response_model=PrescriptionOut)
def create_prescription(data: PrescriptionCreate, db: Session = Depends(get_db)):
    rx = Prescription(**data.dict())
    db.add(rx)
    db.commit()
    db.refresh(rx)
    return rx
