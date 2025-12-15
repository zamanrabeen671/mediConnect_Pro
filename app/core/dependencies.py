"""
Common dependencies for FastAPI endpoints
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .security import get_current_user
from ..models import User


async def get_db_session() -> Session:
    """
    Get database session dependency
    """
    db = get_db()
    return next(db)


async def verify_user_exists(user_id: int, db: Session = Depends(get_db)) -> bool:
    """
    Verify that a user exists by ID
    """
    from ..models import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return True
