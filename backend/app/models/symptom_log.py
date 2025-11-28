from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class SymptomLog(Base):
    __tablename__ = "symptom_logs"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    interaction_id = Column(String, ForeignKey("interaction_logs.id"), nullable=True, index=True)
    llm_request_id = Column(String, ForeignKey("llm_requests.id"), nullable=True, index=True)
    location = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    duration_text = Column(String, nullable=True)
    onset_time = Column(DateTime(timezone=True), nullable=True)
    context = Column(JSONB, nullable=True)
    symptoms_raw = Column(String, nullable=True)
    structured_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
