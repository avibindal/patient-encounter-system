import pytest
from src.database import SessionLocal, engine, Base
from src.models.models import Doctor, Patient


@pytest.fixture(scope="session", autouse=True)
def ensure_db():
    # Ensure tables exist before tests run
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def real_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def doctor(real_db_session):
    doctor = Doctor(name="Dr Test", speciality="General", is_active=True)
    real_db_session.add(doctor)
    real_db_session.commit()
    return doctor


@pytest.fixture
def patient(real_db_session):
    patient = Patient(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        phone_no="1234567890",
        age=30,
    )
    real_db_session.add(patient)
    real_db_session.commit()
    return patient
