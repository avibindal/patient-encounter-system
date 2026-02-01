import pytest
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError

from src.schemas.asch import AppointmentCreate


def make_future(dt=None):
    return (datetime.now(timezone.utc) + timedelta(days=1)) if dt is None else dt


def test_timezone_required_raises():
    with pytest.raises(ValidationError):
        AppointmentCreate(
            patient_id=1,
            doctor_id=1,
            start_time=datetime.now(),
            reason="test",
            dur_min=30,
        )


def test_timezone_valid_passes():
    appt = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) + timedelta(days=1),
        reason="test",
        dur_min=30,
    )
    assert appt.start_time.tzinfo is not None


def test_dur_min_too_small_raises():
    with pytest.raises(ValidationError):
        AppointmentCreate(
            patient_id=1,
            doctor_id=1,
            start_time=make_future(),
            reason="test",
            dur_min=10,
        )


def test_dur_min_boundary_ok():
    appt = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=make_future(),
        reason="test",
        dur_min=15,
    )
    assert appt.dur_min == 15


def test_ids_must_be_positive():
    with pytest.raises(ValidationError):
        AppointmentCreate(
            patient_id=0,
            doctor_id=1,
            start_time=make_future(),
            reason="test",
            dur_min=15,
        )
    with pytest.raises(ValidationError):
        AppointmentCreate(
            patient_id=1,
            doctor_id=0,
            start_time=make_future(),
            reason="test",
            dur_min=15,
        )
