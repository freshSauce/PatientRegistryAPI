from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, BaseResponseModel


class MedicalHistory(Base):
    __tablename__ = 'medical_history'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    date = Column(Integer)
    record_type = Column(String(50))
    description = Column(String(255))

    patient = relationship('Patient', back_populates='medical_records')

class MedicalHistoryModelCreate(BaseResponseModel):
    record_type: str
    description: str

class MedicalHistoryModel(BaseResponseModel):
    id: int
    patient_id: int
    date: int
    record_type: str
    description: str

    class Config:
        from_attributes = True

class MedicalHistoryModelUpdate(BaseResponseModel):
    date: int | None = None
    record_type: str | None = None
    description: str | None = None
