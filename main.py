from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from db.database import Base, engine, get_db
from service import message_service, schemas

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=204)
def root():
    return None


@app.post("/messages/", response_model=schemas.MessageDisplay)
def post_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return message_service.create_message(db, message)


@app.get("/messages/{message_id}", response_model=schemas.MessageDisplay)
def get_message(message_id: int, db: Session = Depends(get_db)):
    db_message = message_service.read_message(db, message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message


@app.put("/messages/{message_id}", response_model=schemas.MessageDisplay)
def put_message(
    message_id: int,
    updated_message: schemas.MessageCreate,
    db: Session = Depends(get_db),
):
    db_message = message_service.read_message(db, message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message_service.update_message(db, db_message, updated_message)


@app.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = message_service.read_message(db, message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message_service.delete_message(db, db_message)


@app.get("/messages/search/", response_model=List[schemas.MessageDisplay])
def search_messages(query: str, db: Session = Depends(get_db)):
    return message_service.search_messages(db, query)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8090)
