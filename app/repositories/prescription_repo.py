"""
Prescription repository - Database access layer for Prescription model
"""
from sqlalchemy.orm import joinedload, Session
from ..models import Prescription, Medicine, PrescriptionMedicine
from ..schemas import PrescriptionCreate, PrescriptionMedicineCreate, MedicineCreate


class PrescriptionRepository:
    """Repository for Prescription database operations"""
    
    @staticmethod
    def create_prescription(db: Session, prescription: PrescriptionCreate) -> Prescription:
        """Create a new prescription and associated prescription medicines"""
        db_prescription = Prescription(
            appointment_id=prescription.appointment_id,
            patient_id=prescription.patient_id,
            notes=prescription.notes
        )
        db.add(db_prescription)
        db.commit()
        db.refresh(db_prescription)

        # handle medicines if provided
        meds = getattr(prescription, "medicines", None) or []
        for med in meds:
            # med can be PrescriptionMedicineCreate
            medicine_id = None
            if getattr(med, "medicine_id", None):
                medicine_id = med.medicine_id
            elif getattr(med, "medicine", None):
                m: MedicineCreate = med.medicine
                # create medicine record if details provided
                db_med = Medicine(
                    name=m.name,
                    strength=m.strength,
                    form=m.form,
                    manufacturer=m.manufacturer
                )
                db.add(db_med)
                db.commit()
                db.refresh(db_med)
                medicine_id = db_med.id

            if medicine_id:
                db_pm = PrescriptionMedicine(
                    prescription_id=db_prescription.id,
                    medicine_id=medicine_id,
                    dosage=getattr(med, "dosage", None),
                    duration=getattr(med, "duration", None),
                    instruction=getattr(med, "instruction", None)
                )
                db.add(db_pm)
        db.commit()
        db.refresh(db_prescription)
        return db_prescription
    
    @staticmethod
    def get_prescription_by_id(db: Session, prescription_id: int) -> Prescription:
        """Get prescription by ID, eager-load medicines and medicine details"""
        return (
            db.query(Prescription)
            .options(joinedload(Prescription.medicines).joinedload(PrescriptionMedicine.medicine))
            .filter(Prescription.id == prescription_id)
            .first()
        )
    
    @staticmethod
    def get_prescription_by_appointment(db: Session, appointment_id: int) -> Prescription:
        """Get prescription by appointment ID"""
        return (
            db.query(Prescription)
            .options(joinedload(Prescription.medicines).joinedload(PrescriptionMedicine.medicine))
            .filter(Prescription.appointment_id == appointment_id)
            .first()
        )
    
    @staticmethod
    def get_prescriptions_by_patient(db: Session, patient_id: int):
        """Get all prescriptions for a patient"""
        return db.query(Prescription).filter(Prescription.patient_id == patient_id).all()
    
    @staticmethod
    def get_all_prescriptions(db: Session, skip: int = 0, limit: int = 100):
        """Get all prescriptions with pagination"""
        return db.query(Prescription).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_prescription(db: Session, prescription_id: int, update_data: dict) -> Prescription:
        """Update prescription"""
        prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
        if prescription:
            for key, value in update_data.items():
                setattr(prescription, key, value)
            db.commit()
            db.refresh(prescription)
        return prescription
    
    @staticmethod
    def delete_prescription(db: Session, prescription_id: int) -> bool:
        """Delete prescription"""
        prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
        if prescription:
            db.delete(prescription)
            db.commit()
            return True
        return False
