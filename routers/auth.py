from typing import Annotated
from datetime import datetime, timedelta, timezone
from os import getenv

from models import User, UserResponseModel, UserResponseModelCreate, UserResponseModelUpdate, UserResponseLogin, Token
from database import DatabaseManager

import jwt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt

router = APIRouter(
    prefix="/auth",
    tags = ["auth"],
    responses={404: {"description": "Not found"}}
    )

db = DatabaseManager()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))
    return encoded_jwt

@router.get("/user/{user_id}")
async def get_user(user_id: int) -> UserResponseModel:
    user = db.get(User, id=user_id)
    if user:
        return user
    raise HTTPException(status_code=404)

@router.post("/register")
async def register_user(user: UserResponseModelCreate) -> dict:
    username = user.username
    email = user.email
    password = bcrypt.hash(user.password)
    user = User(username=username, email=email, password=password)
    db.add(user)
    if db.get(User, username=username):
        return {"message": "user successfully registered"}
    raise HTTPException(status_code=400,
                        detail="Something went wrong while registering, please contact the adminsitrator.")

@router.post("/login")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> Token:
    db_user = db.get(User, username=form_data.username)

    if not db_user:
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    check_password = bcrypt.verify(form_data.password, db_user.password)
    if not check_password:
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
