from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.admin_service import AdminService

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    """Return top-level counts for admin dashboard"""
    return AdminService.get_dashboard_counts(db)


@router.get("/pending-doctors")
def pending_doctors(db: Session = Depends(get_db)):
    doctors = AdminService.list_pending_doctors(db)
    # return minimal doctor info
    return [
        {"id": d.id, "full_name": d.full_name, "phone": d.phone, "status": d.status}
        for d in doctors
    ]


@router.get("/analytics/medicines")
def analytics_top_medicines(limit: int = 10, db: Session = Depends(get_db)):
    rows = AdminService.top_medicines(db, limit)
    return [
        {"medicine": {"id": m.id, "name": m.name, "strength": m.strength, "form": m.form}, "used": int(used)}
        for m, used in rows
    ]


@router.get("/analytics/top-doctors")
def analytics_top_doctors(limit: int = 5, db: Session = Depends(get_db)):
    rows = AdminService.top_doctors_by_completed_appointments(db, limit)
    return [
        {"doctor": {"id": d.id, "full_name": d.full_name, "specialization": d.specialization}, "completed": int(c)}
        for d, c in rows
    ]


@router.get("/analytics/appointments-overview")
def analytics_appointments_overview(days: int = 7, db: Session = Depends(get_db)):
    """Return appointment counts per day for the last `days` days"""
    return AdminService.appointment_overview(db, days)


@router.get("/analytics/specializations")
def analytics_specializations(limit: int = 10, db: Session = Depends(get_db)):
    """Return popular specializations (doctor counts)"""
    rows = AdminService.popular_specializations(db, limit)
    return [{"specialization": spec, "count": int(cnt)} for spec, cnt in rows]
