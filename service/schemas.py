from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    author: str
    body: str
    date: datetime = datetime.utcnow()


class MessageDisplay(BaseModel):
    id: int
    author: str
    date: datetime
    body: str
