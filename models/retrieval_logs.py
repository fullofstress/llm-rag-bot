from sqlalchemy import Column, UUID, ForeignKey, DateTime, Text, ARRAY, Float, Integer
from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from models.base import Base

EMBEDDING_DIM = 384

class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"
    id = Column(UUID, primary_key=True, default=uuid4)

    query = Column(Text, nullable=False)
    query_embedding = Column(Vector(EMBEDDING_DIM), nullable=False)

    top_k_ids = Column(ARRAY(UUID), default=[])

    scores = Column(JSONB, default={})

    latency_ms = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now)
    