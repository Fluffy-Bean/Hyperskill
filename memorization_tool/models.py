from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Cards(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    box = Column(Integer, default=1)
    question = Column(String)
    answer = Column(String)

    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self.answer}"


def create_db(engine):
    Base.metadata.create_all(engine)
