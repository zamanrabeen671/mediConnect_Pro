from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import QualificationCreate, QualificationOut
from ..services.qualification_service import QualificationService

router = APIRouter(prefix="/api/v1/qualifications", tags=["Qualifications"])


@router.post("/", response_model=QualificationOut, status_code=status.HTTP_201_CREATED)
def create_qualification(qualification: QualificationCreate, db: Session = Depends(get_db)):
    return QualificationService.create_qualification(db, qualification)


@router.get("/", response_model=list[QualificationOut])
def list_qualifications(search: Optional[str] = None, db: Session = Depends(get_db)):
    return QualificationService.list_qualifications(db, search)


@router.get("/{qualification_id}", response_model=QualificationOut)
def get_qualification(qualification_id: int, db: Session = Depends(get_db)):
    obj = QualificationService.get_qualification(db, qualification_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Qualification not found")
    return obj


@router.put("/{qualification_id}", response_model=QualificationOut)
def update_qualification(qualification_id: int, update_data: dict, db: Session = Depends(get_db)):
    obj = QualificationService.update_qualification(db, qualification_id, update_data)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Qualification not found")
    return obj


@router.delete("/{qualification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_qualification(qualification_id: int, db: Session = Depends(get_db)):
    QualificationService.delete_qualification(db, qualification_id)
    return None
