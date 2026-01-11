"""
Doctor repository - Database access layer for Doctor model
"""
from sqlalchemy.orm import Session
from ..models import Doctor, Appointment, Patient, Specialization, Institute, Qualification
from ..schemas import DoctorCreate


class DoctorRepository:
    
    @staticmethod
    def create_doctor(db: Session, doctor: DoctorCreate, user_id: int):
        db_doctor = Doctor(
            id=user_id,
            full_name=doctor.full_name,
            phone=doctor.phone,
            bmdc_number=doctor.bmdc_number,
            experience=doctor.experience,
            consultation_fee=doctor.consultation_fee,
            status="pending",
        )

        # associate specializations / institutes / qualifications if provided
        if doctor.specialization_ids:
            specs = db.query(Specialization).filter(Specialization.id.in_(doctor.specialization_ids)).all()
            for s in specs:
                db_doctor.specializations.append(s)

        if doctor.institute_ids:
            insts = db.query(Institute).filter(Institute.id.in_(doctor.institute_ids)).all()
            for i in insts:
                db_doctor.institutes.append(i)

        if doctor.qualification_ids:
            quals = db.query(Qualification).filter(Qualification.id.in_(doctor.qualification_ids)).all()
            for q in quals:
                db_doctor.qualifications.append(q)

        # accept qualification names and create missing ones
        if getattr(doctor, "qualification_names", None):
            for name in doctor.qualification_names:
                name = name.strip()
                if not name:
                    continue
                qobj = db.query(Qualification).filter(Qualification.name == name).first()
                if not qobj:
                    qobj = Qualification(name=name)
                    db.add(qobj)
                    db.commit()
                    db.refresh(qobj)
                if qobj not in db_doctor.qualifications:
                    db_doctor.qualifications.append(qobj)

        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor


    
    @staticmethod
    def get_doctor_by_id(db: Session, doctor_id: int) -> Doctor:
        return db.query(Doctor).filter(Doctor.id == doctor_id).first()
    
    @staticmethod
    def get_all_doctors(db: Session, skip: int = 0, limit: int = 100):
        """Get all doctors with pagination"""
        return db.query(Doctor).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_doctors_by_status(db: Session, status: str):
        """Get doctors by status"""
        return db.query(Doctor).filter(Doctor.status == status).all()
    
    @staticmethod
    def update_doctor(db: Session, doctor_id: int, update_data: dict) -> Doctor:
        """Update doctor"""
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            for key, value in update_data.items():
                setattr(doctor, key, value)
            db.commit()
            db.refresh(doctor)
        return doctor
    
    @staticmethod
    def delete_doctor(db: Session, doctor_id: int) -> bool:
        """Delete doctor"""
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            db.delete(doctor)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_patient_count(db: Session, doctor_id: int) -> int:
        """Get total number of unique patients for a doctor"""
        return db.query(Patient).join(
            Appointment, Appointment.patient_id == Patient.id
        ).filter(
            Appointment.doctor_id == doctor_id
        ).distinct().count()

