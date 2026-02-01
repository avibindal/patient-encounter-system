from pydantic import BaseModel, EmailStr
from datetime import datetime


class PatientCreate(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_no: str
    age: int
    email: EmailStr


class PatientRead(PatientCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
