"""
Admin repository - queries used by admin/dashboard and analytics
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..models import Doctor, Patient, Appointment, PrescriptionMedicine, Medicine
from datetime import date, timedelta


class AdminRepository:

    @staticmethod
    def get_counts(db: Session) -> dict:
        total_doctors = db.query(func.count(Doctor.id)).scalar() or 0
        total_patients = db.query(func.count(Patient.id)).scalar() or 0
        pending_doctors = db.query(func.count(Doctor.id)).filter(Doctor.status == 'pending').scalar() or 0
        total_appointments = db.query(func.count(Appointment.id)).scalar() or 0

        return {
            "total_doctors": int(total_doctors),
            "total_patients": int(total_patients),
            "pending_doctors": int(pending_doctors),
            "total_appointments": int(total_appointments),
        }

    @staticmethod
    def list_pending_doctors(db: Session):
        return db.query(Doctor).filter(Doctor.status == 'pending').all()

    @staticmethod
    def top_medicines(db: Session, limit: int = 10):
        # Count usage of medicines in prescriptions
        q = (
            db.query(Medicine, func.count(PrescriptionMedicine.id).label('used'))
            .join(PrescriptionMedicine, PrescriptionMedicine.medicine_id == Medicine.id)
            .group_by(Medicine.id)
            .order_by(desc('used'))
            .limit(limit)
        )
        return q.all()

    @staticmethod
    def top_doctors_by_completed_appointments(db: Session, limit: int = 5):
        q = (
            db.query(Doctor, func.count(Appointment.id).label('completed'))
            .join(Appointment, Appointment.doctor_id == Doctor.id)
            .filter(Appointment.status == 'completed')
            .group_by(Doctor.id)
            .order_by(desc('completed'))
            .limit(limit)
        )
        return q.all()

    @staticmethod
    def appointment_overview(db: Session, days: int = 7):
        """Return appointment counts grouped by date for the last `days` days."""
        today = date.today()
        start = today - timedelta(days=days - 1)

        q = (
            db.query(Appointment.appointment_date.label('date'), func.count(Appointment.id).label('count'))
            .filter(Appointment.appointment_date >= start)
            .group_by(Appointment.appointment_date)
            .order_by(Appointment.appointment_date)
        )
        results = q.all()
        # Normalize into list of dicts for each day in range (include zeros)
        counts_by_date = {r.date.isoformat(): int(r.count) for r in results}
        out = []
        for i in range(days):
            d = start + timedelta(days=i)
            out.append({"date": d.isoformat(), "count": counts_by_date.get(d.isoformat(), 0)})
        return out

    @staticmethod
    def popular_specializations(db: Session, limit: int = 10):
        """Return top specializations by number of doctors."""
        q = (
            db.query(Doctor.specialization.label('specialization'), func.count(Doctor.id).label('count'))
            .group_by(Doctor.specialization)
            .order_by(desc('count'))
            .limit(limit)
        )
        return q.all()
