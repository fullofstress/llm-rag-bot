from sqlalchemy import Column, Text, UUID, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from models.base import Base
from uuid import uuid4
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID, primary_key=True, default=uuid4)
    title = Column(Text, nullable=False)
    # faq, pdf, web, manual
    source_type = Column(Text, nullable=False)

    source_url = Column(Text, nullable=True)
    meta = Column(JSONB, default={})

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

