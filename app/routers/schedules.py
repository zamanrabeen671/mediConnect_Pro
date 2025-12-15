"""
Schedule routes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ScheduleCreate, ScheduleOut
from ..services.schedule_service import ScheduleService
from ..core.security import get_current_doctor

router = APIRouter(prefix="/schedules", tags=["Schedules"])


@router.post("/", response_model=ScheduleOut, status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_doctor = Depends(get_current_doctor)
):
    """Create a new schedule"""
    return ScheduleService.create_schedule(db, schedule)


@router.get("/{schedule_id}", response_model=ScheduleOut)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Get schedule by ID"""
    return ScheduleService.get_schedule(db, schedule_id)


@router.get("/doctor/{doctor_id}", response_model=list[ScheduleOut])
def get_doctor_schedules(doctor_id: int, db: Session = Depends(get_db)):
    """Get all schedules for a doctor"""
    return ScheduleService.get_doctor_schedules(db, doctor_id)


@router.get("/", response_model=list[ScheduleOut])
def list_schedules(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all schedules"""
    return ScheduleService.list_schedules(db, skip, limit)


@router.put("/{schedule_id}", response_model=ScheduleOut)
def update_schedule(
    schedule_id: int,
    update_data: dict,
    db: Session = Depends(get_db)
):
    """Update schedule"""
    return ScheduleService.update_schedule(db, schedule_id, update_data)


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Delete schedule"""
    ScheduleService.delete_schedule(db, schedule_id)
    return None
