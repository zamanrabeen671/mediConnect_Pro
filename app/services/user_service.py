"""
User service - Business logic for user operations
"""
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


class UserService:
    """Service for user-related business logic"""
    
    @staticmethod
    def register_user(db: Session, user: UserCreate) -> UserOut:
        """
        Register a new user
        
        Args:
            db: Database session
            user: User creation data
        
        Returns:
            Created user
        
        Raises:
            EmailAlreadyExistsException: If email already registered
        """
        # Check if email already exists
        existing_user = UserRepository.get_user_by_email(db, user.email)
        if existing_user:
            raise EmailAlreadyExistsException()
        
        # Hash password
        hashed_password = hash_password(user.password)
        
        # Create user
        new_user = UserRepository.create_user(db, user, hashed_password)
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> dict:
        """
        Authenticate user and return token
        
        Args:
            db: Database session
            email: User email
            password: User password
        
        Returns:
            Dictionary with token and user info
        
        Raises:
            InvalidCredentialsException: If credentials invalid
        """
        # Find user by email
        user = UserRepository.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsException()
        
        # Create access token
        token = create_access_token({"id": user.id, "role": user.role})
        
        return {
            "token": token,
            "user": UserOut.from_orm(user)
        }
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> UserOut:
        """Get user by ID"""
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise Exception("User not found")
        return UserOut.from_orm(user)
    
    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100):
        """List all users"""
        return UserRepository.get_all_users(db, skip, limit)
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user"""
        return UserRepository.delete_user(db, user_id)
