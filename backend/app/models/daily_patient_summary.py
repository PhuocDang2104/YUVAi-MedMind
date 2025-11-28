from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class DailyPatientSummary(Base):
    __tablename__ = "daily_patient_summaries"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    summary_date = Column(Date, nullable=False, index=True)
    total_doses = Column(Integer, default=0, nullable=False)
    on_time = Column(Integer, default=0, nullable=False)
    late = Column(Integer, default=0, nullable=False)
    missed = Column(Integer, default=0, nullable=False)
    symptom_count = Column(Integer, default=0, nullable=False)
    emergency_count = Column(Integer, default=0, nullable=False)
    ai_summary_text = Column(String, nullable=True)
    summary_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
