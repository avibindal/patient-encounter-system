import pytest
import uuid
from fastapi import HTTPException
from src.services.pser import create_patient, get_patient_by_id
from src.schemas.psch import PatientCreate


def test_create_patient_success(real_db_session):
    unique = uuid.uuid4().hex
    data = PatientCreate(
        id=9999,
        first_name="John",
        last_name="Doe",
        phone_no="5551234567",
        age=40,
        email=f"john.doe+{unique}@example.com",
    )
    patient = create_patient(real_db_session, data)
    assert patient.id is not None
    assert patient.email == data.email


def test_create_patient_duplicate_email(real_db_session):
    unique = uuid.uuid4().hex
    data = PatientCreate(
        id=8888,
        first_name="Jane",
        last_name="Smith",
        phone_no="5559876543",
        age=35,
        email=f"jane.smith+{unique}@example.com",
    )
    create_patient(real_db_session, data)
    with pytest.raises(HTTPException) as exc:
        create_patient(real_db_session, data)
    assert exc.value.status_code == 400


def test_get_patient_by_id_not_found(real_db_session):
    with pytest.raises(HTTPException) as exc:
        get_patient_by_id(real_db_session, 999999)
    assert exc.value.status_code == 404


def test_get_patient_by_id_success(real_db_session):
    unique = uuid.uuid4().hex
    data = PatientCreate(
        id=7777,
        first_name="Sam",
        last_name="Green",
        phone_no="5550001111",
        age=28,
        email=f"sam.green+{unique}@example.com",
    )
    created = create_patient(real_db_session, data)
    fetched = get_patient_by_id(real_db_session, created.id)
    assert fetched.email == data.email
