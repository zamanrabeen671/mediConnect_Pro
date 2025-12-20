"""
Routers package initialization
"""
from .auth import router as auth_router
from .users import router as users_router
from .doctors import router as doctors_router
from .patients import router as patients_router
from .schedules import router as schedules_router
from .appointments import router as appointments_router
from .prescriptions import router as prescriptions_router
from .blood_group import router as blood_group_router
__all__ = [
    "auth_router",
    "users_router",
    "doctors_router",
    "patients_router",
    "schedules_router",
    "appointments_router",
    "prescriptions_router",
    "blood_group_router",
]
