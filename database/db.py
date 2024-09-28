from models import Patient # noqa: F401
from models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os

load_dotenv(override=True)

connection_string = os.getenv("DATABASE_CONNECTION_STRING", "localhost:3306")


def create_connector():
    engine = create_engine(connection_string)
    return engine


def create_session(engine):
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return session()

def create_database():
    engine = create_connector()
    Base.metadata.create_all(bind=engine)
    return engine