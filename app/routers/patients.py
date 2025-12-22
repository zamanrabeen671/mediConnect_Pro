"""
Patient routes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import PatientCreate, PatientOut
from ..services.patient_service import PatientService
from ..core.security import get_current_patient

router = APIRouter(prefix="/api/v1/patients", tags=["Patients"])


@router.post("/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    """Create a new patient"""
    return PatientService.create_patient(db, patient, user_id=1)


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get patient by ID"""
    return PatientService.get_patient(db, patient_id)


@router.get("/", response_model=list[PatientOut])
def list_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all patients"""
    return PatientService.list_patients(db, skip, limit)


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: int,
    update_data: dict,
    db: Session = Depends(get_db)
):
    """Update patient information"""
    return PatientService.update_patient(db, patient_id, update_data)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Delete patient"""
    PatientService.delete_patient(db, patient_id)
    return None

