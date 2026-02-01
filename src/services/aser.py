from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from datetime import datetime, timedelta, time

from src.models.models import Appointment, Patient, Doctor

from src.schemas.asch import AppointmentCreate


def has_overlapping_appointment(
    db: Session, doctor_id: int, start_time: datetime, dur_min: int
) -> bool:

    new_end_time = start_time + timedelta(minutes=dur_min)

    overlapping = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.start_time < new_end_time,
            func.addtime(
                Appointment.start_time, func.sec_to_time(Appointment.dur_min * 60)
            )
            > start_time,
        )
        .first()
    )

    return overlapping is not None


def create_appointment(db: Session, appointment_data: AppointmentCreate):
    patient = (
        db.query(Patient).filter(Patient.id == appointment_data.patient_id).first()
    )

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    doctor = db.query(Doctor).filter(Doctor.id == appointment_data.doctor_id).first()

    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor is inactive")

    if appointment_data.start_time < datetime.now(appointment_data.start_time.tzinfo):
        raise HTTPException(
            status_code=400, detail="Appointment must be scheduled in the future"
        )

    if has_overlapping_appointment(
        db,
        appointment_data.doctor_id,
        appointment_data.start_time,
        appointment_data.dur_min,
    ):
        raise HTTPException(
            status_code=409, detail="Doctor already has an overlapping appointment"
        )

    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        start_time=appointment_data.start_time,
        dur_min=appointment_data.dur_min,
        reason=appointment_data.reason,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment


def get_appointments_by_date(db: Session, date, doctor_id: int | None = None):
    # Step 1: start & end of the day
    day_start = datetime.combine(date, time.min)
    day_end = datetime.combine(date, time.max)

    # Step 2: base query (clinic-wide)
    query = db.query(Appointment).filter(
        Appointment.start_time >= day_start, Appointment.start_time <= day_end
    )

    # Step 3: optional doctor filter
    if doctor_id is not None:
        query = query.filter(Appointment.doctor_id == doctor_id)

    # Step 4: return results
    return query.all()
