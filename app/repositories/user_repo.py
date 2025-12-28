from sqlalchemy.orm import Session
from ..models import Patient, User
from ..schemas import UserCreate


class UserRepository:
    
    
    @staticmethod
    def create_user(db: Session, user: UserCreate, hashed_password: str) -> User:
    
        db_user = User(
            email=user.email,
            password=hashed_password,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()
    @staticmethod
    def get_by_phone_or_email(db: Session, value: str):

        return db.query(User).filter(
            (User.phone == value) | (User.email == value)
        ).first()
    
    @staticmethod
    def create_patient_user(db: Session, phone: str, full_name: str):
        user = User(phone=phone, role="patient", password=None)
        db.add(user)
        db.flush()  # to get user.id
        patient = Patient(id=user.id, full_name=full_name, phone=phone)
        db.add(patient)
        db.commit()
        return user

    @staticmethod
    def set_password(db: Session, user: User, password: str):
        user.password = password  # optionally hash
        db.commit()
    @staticmethod
    def update_user(db: Session, user_id: int, update_data: dict) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in update_data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
