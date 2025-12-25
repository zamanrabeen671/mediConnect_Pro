"""
Admin service - business logic for admin/dashboard and analytics
"""
from sqlalchemy.orm import Session
from ..repositories.admin_repo import AdminRepository


class AdminService:

    @staticmethod
    def get_dashboard_counts(db: Session) -> dict:
        return AdminRepository.get_counts(db)

    @staticmethod
    def list_pending_doctors(db: Session):
        return AdminRepository.list_pending_doctors(db)

    @staticmethod
    def top_medicines(db: Session, limit: int = 10):
        return AdminRepository.top_medicines(db, limit)

    @staticmethod
    def top_doctors_by_completed_appointments(db: Session, limit: int = 5):
        return AdminRepository.top_doctors_by_completed_appointments(db, limit)

    @staticmethod
    def appointment_overview(db: Session, days: int = 7):
        return AdminRepository.appointment_overview(db, days)

    @staticmethod
    def popular_specializations(db: Session, limit: int = 10):
        return AdminRepository.popular_specializations(db, limit)
