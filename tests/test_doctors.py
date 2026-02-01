import pytest
from fastapi import HTTPException
from src.services.dser import (
    create_doctor,
    get_doctor_by_id,
    deactivate_doctor,
    activate_doctor,
)
from src.schemas.dsch import DoctorCreate


def test_create_doctor_success(real_db_session):
    data = DoctorCreate(
        id=9999, name="Dr. Alice", speciality="Cardiology", is_active=True
    )
    doctor = create_doctor(real_db_session, data)
    assert doctor.id is not None
    assert doctor.name == data.name


def test_get_doctor_by_id_not_found(real_db_session):
    with pytest.raises(HTTPException) as exc:
        get_doctor_by_id(real_db_session, 999999)
    assert exc.value.status_code == 404


def test_doctor_activation_deactivation(real_db_session):
    data = DoctorCreate(id=8888, name="Dr. Bob", speciality="Neurology", is_active=True)
    doctor = create_doctor(real_db_session, data)
    deactivated = deactivate_doctor(real_db_session, doctor.id)
    assert deactivated.is_active is False
    activated = activate_doctor(real_db_session, doctor.id)
    assert activated.is_active is True
