from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


def create_db(engine):
    Base.metadata.create_all(engine)
