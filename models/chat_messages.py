from sqlalchemy import Column, UUID, ForeignKey, DateTime, Text
from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from models.base import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(UUID, primary_key=True, default=uuid4)
    session_id = Column(UUID, ForeignKey("chat_sessions.id"), nullable=False)
    
    role = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    meta = Column(JSONB, default={})

    created_at = Column(DateTime, default=datetime.now)