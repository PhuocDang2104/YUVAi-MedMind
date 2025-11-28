from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class LLMRequest(Base):
    __tablename__ = "llm_requests"

    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True, index=True)
    interaction_id = Column(String, ForeignKey("interaction_logs.id"), nullable=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=True, index=True)
    device_id = Column(String, ForeignKey("devices.id"), nullable=True, index=True)
    intent = Column(String, nullable=True, index=True)
    input_text = Column(String, nullable=True)
    output_text = Column(String, nullable=True)
    model_name = Column(String, nullable=True)
    latency_ms = Column(String, nullable=True)
    meta = Column("metadata", JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
