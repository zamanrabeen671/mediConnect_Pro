from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut
from ..utils import hash_password
from ..auth import authenticate, create_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)
    new_user = User(email=user.email, password=hashed, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate(email, password, db)
    token = create_token({"id": user.id, "role": user.role})
    return {"token": token, "user": user}
