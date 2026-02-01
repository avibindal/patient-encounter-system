from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.models.models import Patient
from src.schemas.psch import PatientCreate


def create_patient(db: Session, patient_data: PatientCreate):
    existing_patient = (
        db.query(Patient).filter(Patient.email == patient_data.email).first()
    )

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient with this email already exists",
        )

    patient = Patient(
        first_name=patient_data.first_name,
        last_name=patient_data.last_name,
        phone_no=patient_data.phone_no,
        age=patient_data.age,
        email=patient_data.email,
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patient_by_id(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    return patient
