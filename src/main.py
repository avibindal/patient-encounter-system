from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date

from src.database import SessionLocal, engine, Base
from src.schemas.psch import PatientCreate, PatientRead
from src.schemas.dsch import DoctorCreate, DoctorRead
from src.schemas.asch import AppointmentCreate, AppointmentRead

from src.services.pser import create_patient, get_patient_by_id
from src.services.dser import (
    create_doctor,
    get_doctor_by_id,
)
from src.services.aser import (
    create_appointment,
    get_appointments_by_date,
)

# from src.models import models

app = FastAPI(title="Medical Encounter Management System")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/patients", response_model=PatientRead, status_code=201)
def create_patient_api(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db, patient)


@app.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient_api(patient_id: int, db: Session = Depends(get_db)):
    return get_patient_by_id(db, patient_id)


@app.post("/doctors", response_model=DoctorRead, status_code=201)
def create_doctor_api(doctor: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db, doctor)


@app.get("/doctors/{doctor_id}", response_model=DoctorRead)
def get_doctor_api(doctor_id: int, db: Session = Depends(get_db)):
    return get_doctor_by_id(db, doctor_id)


@app.post("/appointments", response_model=AppointmentRead, status_code=201)
def create_appointment_api(
    appointment: AppointmentCreate, db: Session = Depends(get_db)
):
    return create_appointment(db, appointment)


@app.get("/appointments", response_model=list[AppointmentRead])
def get_appointments_api(
    date: date, doctor_id: int | None = None, db: Session = Depends(get_db)
):
    return get_appointments_by_date(db, date, doctor_id)
