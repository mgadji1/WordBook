from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False, unique=True)
    translation = Column(String, nullable=False)