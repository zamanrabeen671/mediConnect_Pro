"""
Schedule service - Business logic for doctor schedule operations
"""
from sqlalchemy.orm import Session
from ..models import DoctorSchedule
from ..schemas import ScheduleCreate, ScheduleOut
from ..repositories.schedule_repo import ScheduleRepository


class ScheduleService:
    """Service for schedule-related business logic"""
    
    @staticmethod
    def create_schedule(db: Session, schedule: ScheduleCreate) -> ScheduleOut:
        """Create a new schedule"""
        new_schedule = ScheduleRepository.create_schedule(db, schedule)
        return ScheduleOut.from_orm(new_schedule)
    
    @staticmethod
    def get_schedule(db: Session, schedule_id: int) -> ScheduleOut:
        """Get schedule by ID"""
        schedule = ScheduleRepository.get_schedule_by_id(db, schedule_id)
        if not schedule:
            raise Exception("Schedule not found")
        return ScheduleOut.from_orm(schedule)
    
    @staticmethod
    def get_doctor_schedules(db: Session, doctor_id: int):
        """Get all schedules for a doctor"""
        return ScheduleRepository.get_schedules_by_doctor(db, doctor_id)
    
    @staticmethod
    def list_schedules(db: Session, skip: int = 0, limit: int = 100):
        """List all schedules"""
        return ScheduleRepository.get_all_schedules(db, skip, limit)
    
    @staticmethod
    def update_schedule(db: Session, schedule_id: int, update_data: dict) -> ScheduleOut:
        """Update schedule"""
        schedule = ScheduleRepository.update_schedule(db, schedule_id, update_data)
        if not schedule:
            raise Exception("Schedule not found")
        return ScheduleOut.from_orm(schedule)
    
    @staticmethod
    def delete_schedule(db: Session, schedule_id: int) -> bool:
        """Delete schedule"""
        return ScheduleRepository.delete_schedule(db, schedule_id)
