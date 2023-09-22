from enum import StrEnum, auto

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from db.database import Base


class Color(StrEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(63), nullable=False, unique=True)
    password = Column(String(511), nullable=False)
    age = Column(Integer, nullable=False)

    articles = relationship("Article", back_populates="user")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(511), nullable=False)
    color = Column(Enum(Color), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="articles")
