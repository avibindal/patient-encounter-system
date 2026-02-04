from sqlalchemy import (
    # create_engine,
    String,
    Integer,
    ForeignKey,
    # select,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    # sessionmaker
)
from datetime import datetime
from sqlalchemy.sql import func
from src.database import Base

print("imported")


class Patient(Base):
    """
    Represents a patient in the hospital.
    """

    __tablename__ = "patientsavi"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_no: Mapped[str] = mapped_column(String(15), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # One-to-many relationship: one patient -> many appointments
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patient", cascade="save-update, merge"
    )


class Doctor(Base):
    """
    Represents a doctor in the hospital.
    """

    __tablename__ = "avidoctors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    speciality: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    appointments: Mapped[list["Appointment"]] = relationship(back_populates="doctor")


class Appointment(Base):
    """
    Represents an appointment between a patient and a doctor.
    """

    __tablename__ = "appointmentsavi"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patientsavi.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("avidoctors.id"))
    reason: Mapped[str] = mapped_column(String(200))
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    patient: Mapped[Patient] = relationship(back_populates="appointments")
    doctor: Mapped[Doctor] = relationship(back_populates="appointments")
