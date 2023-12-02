from typing import Type

from sqlalchemy.orm import Session

from db.message_dao import Message
from service import schemas


def create_message(db: Session, message: schemas.MessageCreate) -> Message:
    db_message = Message(author=message.author, body=message.body, date=message.date)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def read_message(db: Session, message_id: int) -> Type[Message]:
    return db.query(Message).filter(Message.id == message_id).first()


def update_message(
    db: Session, original_message: Type[Message], updated_message: schemas.MessageCreate
) -> Type[Message]:
    original_message.author = updated_message.author
    original_message.body = updated_message.body
    original_message.date = updated_message.date
    db.commit()
    db.refresh(original_message)
    return original_message


def delete_message(db: Session, message: Type[Message]) -> None:
    db.delete(message)
    db.commit()


def search_messages(db: Session, query: str) -> list[Type[Message]]:
    return db.query(Message).filter(Message.body.ilike(f"%{query}%")).all()
