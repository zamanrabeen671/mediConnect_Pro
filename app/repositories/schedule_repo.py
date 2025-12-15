"""
Schedule repository - Database access layer for DoctorSchedule model
"""
from sqlalchemy.orm import Session
from ..models import DoctorSchedule
from ..schemas import ScheduleCreate


class ScheduleRepository:
    """Repository for DoctorSchedule database operations"""
    
    @staticmethod
    def create_schedule(db: Session, schedule: ScheduleCreate) -> DoctorSchedule:
        """Create a new schedule"""
        db_schedule = DoctorSchedule(
            doctor_id=schedule.doctor_id,
            day_of_week=schedule.day_of_week,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            max_patients=schedule.max_patients
        )
        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)
        return db_schedule
    
    @staticmethod
    def get_schedule_by_id(db: Session, schedule_id: int) -> DoctorSchedule:
        """Get schedule by ID"""
        return db.query(DoctorSchedule).filter(DoctorSchedule.id == schedule_id).first()
    
    @staticmethod
    def get_schedules_by_doctor(db: Session, doctor_id: int):
        """Get all schedules for a doctor"""
        return db.query(DoctorSchedule).filter(DoctorSchedule.doctor_id == doctor_id).all()
    
    @staticmethod
    def get_all_schedules(db: Session, skip: int = 0, limit: int = 100):
        """Get all schedules with pagination"""
        return db.query(DoctorSchedule).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_schedule(db: Session, schedule_id: int, update_data: dict) -> DoctorSchedule:
        """Update schedule"""
        schedule = db.query(DoctorSchedule).filter(DoctorSchedule.id == schedule_id).first()
        if schedule:
            for key, value in update_data.items():
                setattr(schedule, key, value)
            db.commit()
            db.refresh(schedule)
        return schedule
    
    @staticmethod
    def delete_schedule(db: Session, schedule_id: int) -> bool:
        """Delete schedule"""
        schedule = db.query(DoctorSchedule).filter(DoctorSchedule.id == schedule_id).first()
        if schedule:
            db.delete(schedule)
            db.commit()
            return True
        return False
