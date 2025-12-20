
from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ScheduleCreate, ScheduleOut, ScheduleCreateInternal
from ..services.schedule_service import ScheduleService
from ..core.security import get_current_doctor

router = APIRouter(prefix="/api/v1/schedules", tags=["Schedules"])


@router.post("/", response_model=ScheduleOut, status_code=status.HTTP_201_CREATED)
def create_schedule(
    request: Request,
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
):
    user_id = getattr(request.state, "user_id", None)
    user_role = getattr(request.state, "user_role", None)

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if user_role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can create schedules")

    schedule_internal = ScheduleCreateInternal(
        **schedule.dict(),
        doctor_id=user_id
    )

    return ScheduleService.create_schedule(db, schedule_internal)


@router.get("/{schedule_id}", response_model=ScheduleOut)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Get schedule by ID"""
    return ScheduleService.get_schedule(db, schedule_id)


@router.get("/doctor/{doctor_id}", response_model=list[ScheduleOut])
def get_doctor_schedules(doctor_id: int, db: Session = Depends(get_db)):
    """Get all schedules for a doctor"""
    return ScheduleService.get_doctor_schedules(db, doctor_id)


@router.get("/me", response_model=int)
def get_my_schedules(request: Request, db: Session = Depends(get_db)):

    user_id = getattr(request.state, "user_id", None)
    user_role = getattr(request.state, "user_role", None)

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if user_role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can view their schedules")

    return ScheduleService.get_doctor_schedules_id(db, user_id)


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
