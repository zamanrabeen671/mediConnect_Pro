from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import SpecializationCreate, SpecializationOut
from ..services.specialization_service import SpecializationService

router = APIRouter(prefix="/api/v1/specializations", tags=["Specializations"])


@router.post("/", response_model=SpecializationOut, status_code=status.HTTP_201_CREATED)
def create_specialization(specialization: SpecializationCreate, db: Session = Depends(get_db)):
    return SpecializationService.create_specialization(db, specialization)


@router.get("/", response_model=list[SpecializationOut])
def list_specializations(search: str | None = None, db: Session = Depends(get_db)):
    return SpecializationService.list_specializations(db, search)


@router.get("/{specialization_id}", response_model=SpecializationOut)
def get_specialization(specialization_id: int, db: Session = Depends(get_db)):
    obj = SpecializationService.get_specialization(db, specialization_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specialization not found")
    return obj


@router.put("/{specialization_id}", response_model=SpecializationOut)
def update_specialization(specialization_id: int, update_data: dict, db: Session = Depends(get_db)):
    obj = SpecializationService.update_specialization(db, specialization_id, update_data)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specialization not found")
    return obj


@router.delete("/{specialization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_specialization(specialization_id: int, db: Session = Depends(get_db)):
    SpecializationService.delete_specialization(db, specialization_id)
    return None
