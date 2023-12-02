from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    body = Column(String)
