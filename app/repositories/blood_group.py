from sqlalchemy.orm import Session
from ..models import BloodGroup
from ..schemas import BloodGroupCreate

class BloodGroupRepository:
    @staticmethod
    def create(db: Session, blood_group: BloodGroupCreate) -> BloodGroup:
        new_group = BloodGroup(group_name=blood_group.group_name)
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        return new_group

    @staticmethod
    def get_all(db: Session):
        return db.query(BloodGroup).all()
