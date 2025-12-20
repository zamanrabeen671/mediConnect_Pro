# app/routers/blood_group.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import BloodGroupCreate, BloodGroupOut
from ..services.blood_group_service import BloodGroupService

router = APIRouter(prefix="/api/v1/blood-groups", tags=["Blood Groups"])

@router.post("/", response_model=BloodGroupOut, status_code=status.HTTP_201_CREATED)
def create_blood_group(blood_group: BloodGroupCreate, db: Session = Depends(get_db)):
    return BloodGroupService.create_blood_group(db, blood_group)

@router.get("/", response_model=list[BloodGroupOut])
def list_blood_groups(db: Session = Depends(get_db)):
    return BloodGroupService.get_all_blood_groups(db)
