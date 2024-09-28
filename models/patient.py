from sqlalchemy import Column, Integer, String

from .base import Base, BaseResponseModel

class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))

class PatientResponseModelCreate(BaseResponseModel):
    first_name: str
    last_name: str

class PatientResponseModel(BaseResponseModel):
    id: int | None = None
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class PatientResponseModelUpdate(BaseResponseModel):
    first_name: str | None = None
    last_name: str | None = None