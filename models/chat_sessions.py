from sqlalchemy import Column, UUID, ForeignKey, DateTime, Text
from models.base import Base
from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(UUID, primary_key=True, default=uuid4)
    
    # user_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    summary = Column(Text, nullable=True)

    meta = Column(JSONB, default={})

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now) 