from sqlalchemy import select 
from sqlalchemy.orm import Session 

from models import FAQItem
from embeddings import generate_embeddings

def search_faq(question: str, db: Session):
    embedding = generate_embeddings(question)

    similarity = (
        1 - FAQItem.embedding.cosine_distance(embedding)
    ).label("similarity")

    stmt = (
        select(FAQItem, similarity)
        .order_by(
            FAQItem.embedding.cosine_distance(embedding)
        )
        .limit(1)
    )

    result = db.execute(stmt).first()

    if not result:
        return None

    faq, similarity_score = result

    return {
        "id": faq.id,
        "question": faq.question,
        "answer": faq.answer,
        "similarity": float(similarity_score)
    }