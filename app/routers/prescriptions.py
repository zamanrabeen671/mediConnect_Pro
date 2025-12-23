"""
Prescription routes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import PrescriptionCreate, PrescriptionOut
from ..services.prescription_service import PrescriptionService
from ..core.security import get_current_doctor

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


@router.post("/", response_model=PrescriptionOut, status_code=status.HTTP_201_CREATED)
def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_doctor = Depends(get_current_doctor)
):
    """Create a new prescription"""
    return PrescriptionService.create_prescription(db, prescription, current_doctor)


@router.get("/{prescription_id}", response_model=PrescriptionOut)
def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    """Get prescription by ID"""
    return PrescriptionService.get_prescription(db, prescription_id)


@router.get("/appointment/{appointment_id}", response_model=PrescriptionOut)
def get_prescription_by_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Get prescription by appointment ID"""
    return PrescriptionService.get_prescription_by_appointment(db, appointment_id)


@router.get("/patient/{patient_id}", response_model=list[PrescriptionOut])
def get_patient_prescriptions(patient_id: int, db: Session = Depends(get_db)):
    """Get all prescriptions for a patient"""
    return PrescriptionService.get_patient_prescriptions(db, patient_id)


@router.get("/", response_model=list[PrescriptionOut])
def list_prescriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all prescriptions"""
    return PrescriptionService.list_prescriptions(db, skip, limit)


@router.put("/{prescription_id}", response_model=PrescriptionOut)
def update_prescription(
    prescription_id: int,
    update_data: dict,
    db: Session = Depends(get_db)
):
    """Update prescription"""
    return PrescriptionService.update_prescription(db, prescription_id, update_data)


@router.delete("/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    """Delete prescription"""
    PrescriptionService.delete_prescription(db, prescription_id)
    return None
