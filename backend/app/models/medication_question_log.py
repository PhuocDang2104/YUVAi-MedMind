from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class MedicationQuestionLog(Base):
    __tablename__ = "medication_question_logs"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    interaction_id = Column(String, ForeignKey("interaction_logs.id"), nullable=True, index=True)
    llm_request_id = Column(String, ForeignKey("llm_requests.id"), nullable=True, index=True)
    med_name = Column(String, nullable=True)
    question_type = Column(String, nullable=True)
    time_scope = Column(String, nullable=True)
    question_text = Column(String, nullable=True)
    structured_json = Column(JSONB, nullable=True)
    ai_answer_text = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
