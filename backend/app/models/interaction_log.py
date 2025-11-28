from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=True, index=True)
    device_id = Column(String, ForeignKey("devices.id"), nullable=True, index=True)
    speaker = Column(String, nullable=False)  # PATIENT/SYSTEM/CAREGIVER
    source = Column(String, nullable=False)  # VOICE/MANUAL/DEVICE
    text_raw = Column(String, nullable=True)
    text_normalized = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    meta = Column("metadata", JSONB, nullable=True)  # stored as metadata column name, avoid reserved attr
    created_at = Column(DateTime(timezone=True), server_default=func.now())
