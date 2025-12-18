"""
Authentication routes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserCreate, UserOut, LoginRequest
from ..services.user_service import UserService

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    return UserService.register_user(db, user)


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    
    return UserService.authenticate_user(db, user.email, user.password)