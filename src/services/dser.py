from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.models.models import Doctor
from src.schemas.dsch import DoctorCreate


def create_doctor(db: Session, doctor_data: DoctorCreate):
    doctor = Doctor(
        name=doctor_data.name,
        speciality=doctor_data.speciality,
        is_active=doctor_data.is_active,
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def get_doctor_by_id(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="doctor not found"
        )

    return doctor


def deactivate_doctor(db: Session, doctor_id: int):
    doctor = get_doctor_by_id(db, doctor_id)

    doctor.is_active = False
    db.commit()
    db.refresh(doctor)

    return doctor


def activate_doctor(db: Session, doctor_id: int):
    doctor = get_doctor_by_id(db, doctor_id)

    doctor.is_active = True
    db.commit()
    db.refresh(doctor)

    return doctor
