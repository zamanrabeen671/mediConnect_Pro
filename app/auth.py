from datetime import datetime, timedelta
from jose import jwt
from .utils import verify_password
from fastapi import HTTPException, Depends
from .database import get_db
from sqlalchemy.orm import Session
from .models import User

SECRET_KEY = "mysecret"
ALGO = "HS256"


def create_token(data: dict):
    data.update({"exp": datetime.utcnow() + timedelta(hours=6)})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGO)


def authenticate(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
