from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, time, timezone

from src.models.models import Appointment, Patient, Doctor

from src.schemas.asch import AppointmentCreate


def has_overlapping_appointment(
    db: Session, doctor_id: int, start_time: datetime, duration: int
) -> bool:

    # Compute the new appointment end time in Python
    new_end_time = start_time + timedelta(minutes=duration)

    # Fetch candidate appointments for the doctor that start before the new end time.
    # Then perform an explicit overlap check in Python to avoid DB-specific SQL
    # functions (works with SQLite, MySQL, etc.). This is efficient enough for
    # typical clinic loads and keeps behavior consistent across DB backends.
    candidates = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id, Appointment.start_time < new_end_time
        )
        .all()
    )

    # Ensure comparisons are done with datetimes that share the same tzinfo.
    tz = start_time.tzinfo or timezone.utc

    for appt in candidates:
        # Normalize stored appointment start_time to the same timezone as the input start_time
        if appt.start_time is None:
            continue
        if appt.start_time.tzinfo is None:
            appt_start = appt.start_time.replace(tzinfo=tz)
        else:
            appt_start = appt.start_time.astimezone(tz)

        appt_end = appt_start + timedelta(minutes=appt.duration)

        # Overlap exists when existing appt starts before new end and ends after new start
        if appt_start < new_end_time and appt_end > start_time:
            return True

    return False


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
        appointment_data.duration,
    ):
        raise HTTPException(
            status_code=409, detail="Doctor already has an overlapping appointment"
        )

    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        start_time=appointment_data.start_time,
        duration=appointment_data.duration,
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
