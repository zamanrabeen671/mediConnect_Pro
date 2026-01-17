from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import InstituteCreate, InstituteOut
from ..services.institute_service import InstituteService

router = APIRouter(prefix="/api/v1/institutes", tags=["Institutes"])


@router.post("/", response_model=InstituteOut, status_code=status.HTTP_201_CREATED)
def create_institute(institute: InstituteCreate, db: Session = Depends(get_db)):
    return InstituteService.create_institute(db, institute)


@router.get("/", response_model=list[InstituteOut])
def list_institutes(search: Optional[str] = None, db: Session = Depends(get_db)):
    return InstituteService.list_institutes(db, search)


@router.get("/{institute_id}", response_model=InstituteOut)
def get_institute(institute_id: int, db: Session = Depends(get_db)):
    obj = InstituteService.get_institute(db, institute_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institute not found")
    return obj


@router.put("/{institute_id}", response_model=InstituteOut)
def update_institute(institute_id: int, update_data: dict, db: Session = Depends(get_db)):
    obj = InstituteService.update_institute(db, institute_id, update_data)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institute not found")
    return obj


@router.delete("/{institute_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_institute(institute_id: int, db: Session = Depends(get_db)):
    InstituteService.delete_institute(db, institute_id)
    return None
