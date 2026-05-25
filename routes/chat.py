from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from services.retrieval import RetrievalService
from services.llm import LLMService

router = APIRouter()

retrieval = RetrievalService()
llm = LLMService()

@router.post("/chat")
def chat(question: str, db: Session = Depends(get_db)):
    results = retrieval.search(db, question)
    
    contexts = [r.content for r in results]

    answer = llm.generate_answer(question, contexts)

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "content": r.content,
                "score": r.score,
            } for r in results
        ]
    }
    