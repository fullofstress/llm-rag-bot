from sqlalchemy import Column, Integer, Text 
from models.base import Base
from pgvector.sqlalchemy import Vector

EMBEDDING_DIM = 384

class FAQItem(Base):
    __tablename__ = "faq_items"
    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    embedding = Column(Vector(EMBEDDING_DIM), nullable=False)