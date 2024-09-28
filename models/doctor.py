from sqlalchemy import Column, Integer, String

from .base import Base, BaseResponseModel

class Doctor(Base):
    __tablename__ = 'doctor'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))

class DoctorResponseModelCreate(BaseResponseModel):
    first_name: str
    last_name: str

class DoctorResponseModel(BaseResponseModel):
    id: int | None = None
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class DoctorResponseModelUpdate(BaseResponseModel):
    first_name: str | None = None
    last_name: str | None = None