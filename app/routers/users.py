"""
User routes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserOut
from ..services.user_service import UserService
from ..core.security import get_current_user
from ..models import User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService.get_user(db, current_user.id)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    
    return UserService.get_user(db, user_id)


@router.get("/", response_model=list[UserOut])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all users"""
    return UserService.list_users(db, skip, limit)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user (admin only)"""
    UserService.delete_user(db, user_id)
    return None

@router.post("/patient/signin", response_model=UserOut)
def login_or_create_patient(
    firebase_token: str,
    full_name: str = None,
    db: Session = Depends(get_db)
):
    return UserService.login_or_create_patient(db, firebase_token, full_name)   

@router.post("/patient/verify", status_code=status.HTTP_200_OK)
def verify_patient_phone(
    phone: str,
    db: Session = Depends(get_db),
):
    """Send verification code to patient's phone"""
    UserService.verify_firebase_token(db,phone)
    return {"message": "Verification code sent"}        


