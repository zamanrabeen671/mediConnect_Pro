"""
Medicine routes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import MedicineCreate, MedicineOut
from ..services.medicine_service import MedicineService

router = APIRouter(prefix="/api/v1/medicines", tags=["Medicines"])


@router.post("/", response_model=MedicineOut, status_code=status.HTTP_201_CREATED)
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    return MedicineService.create_medicine(db, medicine)


@router.get("/{medicine_id}", response_model=MedicineOut)
def get_medicine(medicine_id: int, db: Session = Depends(get_db)):
    return MedicineService.get_medicine(db, medicine_id)


@router.get("/", response_model=list[MedicineOut])
def list_medicines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return MedicineService.list_medicines(db, skip, limit)


@router.get("/search/{name}", response_model=list[MedicineOut])
def list_medicines_by_name(name: str, db: Session = Depends(get_db)):
    return MedicineService.list_medicines_by_name(db, name)


@router.put("/{medicine_id}", response_model=MedicineOut)
def update_medicine(medicine_id: int, update_data: dict, db: Session = Depends(get_db)):
    return MedicineService.update_medicine(db, medicine_id, update_data)


@router.delete("/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    MedicineService.delete_medicine(db, medicine_id)
    return None
