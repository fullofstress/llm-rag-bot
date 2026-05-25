from fastapi import FastAPI
from routes import chat, admin
from search import search_faq
from db import get_db

from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/ask")
def ask(question: str, db: Session = Depends(get_db)):
    result = search_faq(question, db)

    return result

app.include_router(chat.router)
app.include_router(admin.router)