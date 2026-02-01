from pydantic import BaseModel, Field
from datetime import datetime


class DoctorCreate(BaseModel):
    id: int
    name: str
    speciality: str
    is_active: bool = Field(default=True)


class DoctorRead(DoctorCreate):
    id: int
    name: str
    speciality: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
