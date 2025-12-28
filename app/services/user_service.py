from http.client import HTTPException
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate, UserOut
from ..repositories.user_repo import UserRepository
from ..utils import hash_password, verify_password
from ..exceptions.http_exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException
)
from ..core.security import create_access_token
from firebase_admin import auth as firebase_auth


class UserService:
    
    @staticmethod
    def register_user(db: Session, user: UserCreate) -> UserOut:
        
        existing_user = UserRepository.get_user_by_email(db, user.email)
        if existing_user:
            raise EmailAlreadyExistsException()
        
        hashed_password = hash_password(user.password)
        
        new_user = UserRepository.create_user(db, user, hashed_password)
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> dict:
        
        user = UserRepository.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsException()
        
        token = create_access_token({"id": user.id, "role": user.role})
        
        if user.role == "doctor":
            from .doctor_service import DoctorService
            doctor = DoctorService.get_doctor(db, user.id)
            user.status = doctor.status if doctor else None

        return {
            "token": token,
            "user": UserOut.from_orm(user)
        }
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> UserOut:
        """Get user by ID"""
        user = UserRepository.get_user_by_id(db, user_id)
        if user.role == "doctor":
            from .doctor_service import DoctorService
            doctor = DoctorService.get_doctor(db, user.id)
            user.status = doctor.status
        if not user:
            raise Exception("User not found")
        return user
    
    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100):
        """List all users"""
        return UserRepository.get_all_users(db, skip, limit)
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user"""
        return UserRepository.delete_user(db, user_id)
    
    @staticmethod
    def verify_firebase_token(db: Session, id_token: str):
        try:
            decoded = firebase_auth.verify_id_token(id_token)
            uid = decoded["uid"]
            phone = decoded.get("phone_number")
            return phone
        except Exception:
            raise HTTPException(401, "Invalid Firebase token")
        
    @staticmethod
    def login_or_create_patient(db: Session, firebase_token: str, full_name: str = None):
        phone = UserService.verify_firebase_token(db, firebase_token)
        user_repo = UserRepository(db)

        user = user_repo.get_by_phone_or_email(phone)
        if user:
            # existing patient, return user
            return user
        else:
            if not full_name:
                raise HTTPException(400, "Full name required for new patient")
            # create patient if not exists
            return user_repo.create_patient_user(phone, full_name)
