import pytest
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from src.services.aser import (
    has_overlapping_appointment,
    create_appointment,
    get_appointments_by_date,
)
from src.schemas.asch import AppointmentCreate


def test_no_conflict(real_db_session, doctor, patient):
    start_time = datetime.now(timezone.utc) + timedelta(hours=2)
    data = AppointmentCreate(
        patient_id=patient.id,
        doctor_id=doctor.id,
        start_time=start_time,
        dur_min=30,
        reason="Routine",
    )
    appointment = create_appointment(real_db_session, data)
    assert appointment.id is not None
    assert not has_overlapping_appointment(
        real_db_session, doctor.id, start_time + timedelta(hours=1), 30
    )


def test_conflict_detected(real_db_session, doctor, patient):
    start_time = datetime.now(timezone.utc) + timedelta(hours=3)
    data1 = AppointmentCreate(
        patient_id=patient.id,
        doctor_id=doctor.id,
        start_time=start_time,
        dur_min=60,
        reason="Consult",
    )
    data2 = AppointmentCreate(
        patient_id=patient.id,
        doctor_id=doctor.id,
        start_time=start_time + timedelta(minutes=30),
        dur_min=30,
        reason="Overlap",
    )
    create_appointment(real_db_session, data1)
    with pytest.raises(HTTPException):
        create_appointment(real_db_session, data2)


def test_get_appointments_by_date(real_db_session, doctor, patient):
    # schedule for tomorrow to avoid intermittently falling into the past
    today = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    start_time = datetime.combine(
        today, datetime.min.time(), tzinfo=timezone.utc
    ) + timedelta(hours=10)
    data = AppointmentCreate(
        patient_id=patient.id,
        doctor_id=doctor.id,
        start_time=start_time,
        dur_min=30,
        reason="Morning",
    )
    create_appointment(real_db_session, data)
    appts = get_appointments_by_date(real_db_session, today, doctor.id)
    assert any(a.start_time.date() == today for a in appts)


def test_appointment_in_past_rejected(real_db_session, doctor, patient):
    start_time = datetime.now(timezone.utc) - timedelta(days=1)
    data = AppointmentCreate(
        patient_id=patient.id,
        doctor_id=doctor.id,
        start_time=start_time,
        dur_min=30,
        reason="Past",
    )
    with pytest.raises(HTTPException):
        create_appointment(real_db_session, data)
