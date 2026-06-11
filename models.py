from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String(36), index=True)
    role = Column(String(50))
    text = Column(Text)
    tools_used = Column(JSON, nullable=True)
    chart_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
