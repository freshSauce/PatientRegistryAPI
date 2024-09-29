from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, BaseResponseModel
from .record import MedicalHistoryModel


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))

    medical_records = relationship('MedicalHistory', back_populates='patient')


class PatientResponseModelCreate(BaseResponseModel):
    first_name: str
    last_name: str

class PatientResponseModel(BaseResponseModel):
    id: int | None = None
    first_name: str
    last_name: str
    medical_records: list[MedicalHistoryModel] = []

    class Config:
        orm_mode = True

class PatientResponseModelUpdate(BaseResponseModel):
    first_name: str | None = None
    last_name: str | None = None
