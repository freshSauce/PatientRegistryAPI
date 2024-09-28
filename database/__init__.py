from .db import create_database, create_session
from models import Patient
import logging

logging.basicConfig(
     filename="app.log",
     encoding="utf-8",
     filemode="a",
     format="{asctime} - {levelname} - {message}",
     style="{",
     datefmt="%Y-%m-%d %H:%M",
 )


class DatabaseManager:
    def __init__(self):
        self.engine = create_database()
        self.session = None
        self.create_session()
        self.tables = {
            "patient": Patient
        }

    def create_session(self):
        self.session = create_session(self.engine)

    def __enter__(self):
        if not self.session:
            self.session = self.create_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        self.session.close()

    def add(self, obj):
        """Summary

        Keyword arguments:\n
        obj -- Instance of the model to be added\n
        Return: None

        Example:
        db = DatabaseManager()\n
        user = db.tables["users"](name="John Doe" ...)

        db.add(user)
        """

        self.session.add(obj)
        self.session.commit()

    def get(self, model, **kwargs):
        """Summary

        Keyword arguments:\n
        model -- Model of the table to be queried\n
        **kwargs -- Arguments to filter the query\n
        Return: First element of the query

        Example:
        db = DatabaseManager()\n

        user = db.get(db.tables["users"], name="John Doe")
        """
        while True:
            try:
                return self.session.query(model).filter_by(**kwargs).first()
            except Exception as e:
                logging.error(f"Error on get on DatabaseManager, doing rollback.", exc_info=True)
                self.session.rollback()


    def get_all_by(self, model, **kwargs):
        """Summary

        Keyword arguments:\n
        model -- Model of the table to be queried\n
        **kwargs -- Arguments to filter the query\n
        Return: All elements of the query

        Example:
        db = DatabaseManager()\n

        user = db.get_all_by(db.tables["users"], name="John Doe")
        """
        while True:
            try:
                return self.session.query(model).filter_by(**kwargs).all()
            except Exception as e:
                logging.error(f"Error on get_all_by on DatabaseManager, doing rollback.", exc_info=True)
                self.session.rollback()
    def get_all(self, model):
        """Summary

        Keyword arguments:\n
        model -- Model of the table to be queried\n
        Return: All elements of the queried table

        Example:
        db = DatabaseManager()\n

        user = db.get_all(db.tables["users"])
        """
        while True:
            try:
                return self.session.query(model).all()
            except Exception as e:
                logging.error(f"Error on get_all on DatabaseManager, doing rollback.", exc_info=True)
                self.session.rollback()

    def update(self, model, element, **kwargs):
        """Summary
        Keyword arguments:\n
        model -- Model of the table to be queried\n
        element -- Element to be updated\n
        **kwargs -- Values to be updated\n
        Return: None

        Example:
        db = DatabaseManager()\n

        user = db.get(db.tables["users"], name="John Doe")\n
        db.update(db.tables["users"], user, name="Jane Doe")
        """
        while True:
            try:
                _id = element.id
                self.session.query(model).filter_by(id=_id).update(kwargs)
                self.session.commit()
                return True
            except Exception as e:
                logging.error(f"Error on update on DatabaseManager, doing rollback.", exc_info=True)
                self.session.rollback()
    def delete(self, obj):
        """Summary
        Keyword arguments:\n
        obj -- Instance to be deleted\n
        Return: None

        Example:
        db = DatabaseManager()\n

        user = db.get(db.tables["users"], name="John Doe")\n
        db.delete(user)
        """
        self.session.delete(obj)
        self.session.commit()

    def flush(self):
        """Summary
        Flush the session
        """
        self.session.flush()
        self.session.commit()