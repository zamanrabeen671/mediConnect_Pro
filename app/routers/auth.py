"""
Authentication routes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserCreate, UserOut
from ..services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return UserService.register_user(db, user)


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login user and get access token"""
    return UserService.authenticate_user(db, email, password)
