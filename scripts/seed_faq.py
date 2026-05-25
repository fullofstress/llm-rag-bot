import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sentence_transformers import SentenceTransformer

from models import FAQItem
import os
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

engine = create_engine(os.getenv("DATABASE_URL"))

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

with open("data/faq.json", "r") as f:
    faqs = json.load(f)

for faq in faqs:
    embedding = model.encode(faq["question"]).tolist()

    item = FAQItem(
        question=faq["question"],
        answer=faq["answer"],
        embedding=embedding
    )

    session.add(item)

session.commit()

print("FAQ data inserted successfully")