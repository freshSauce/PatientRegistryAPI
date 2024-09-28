from sqlalchemy import Column, String, Integer
from .base import Base, BaseResponseModel

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String(25), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(50), unique=True, nullable=False)

class UserResponseModelCreate(BaseResponseModel):
    username: str
    password: str
    email: str

class Token(BaseResponseModel):
    access_token: str
    token_type: str

class UserResponseModel(BaseResponseModel):
    id: int | None = None
    username: str
    email: str

    class Config:
        orm_mode = True

class UserResponseLogin(BaseResponseModel):
    username: str
    password: str


class UserResponseModelUpdate(BaseResponseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


