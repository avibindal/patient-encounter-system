from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class AppointmentCreate(BaseModel):
    patient_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    start_time: datetime
    reason: str
    duration: int = Field(ge=15, le=180)

    @field_validator("start_time")
    @classmethod
    def check_timezone(cls, value):
        if value.tzinfo is None:
            raise ValueError("starttime must include formatting")
        return value


class AppointmentRead(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    start_time: datetime
    duration: int
    created_at: datetime

    class Config:
        from_attributes = True
