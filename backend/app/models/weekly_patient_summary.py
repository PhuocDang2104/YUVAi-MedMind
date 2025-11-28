from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class WeeklyPatientSummary(Base):
    __tablename__ = "weekly_patient_summaries"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    week_start = Column(Date, nullable=False, index=True)
    adherence_rate = Column(String, nullable=True)
    missed_dose_count = Column(Integer, default=0, nullable=False)
    symptom_highlights = Column(JSONB, nullable=True)
    ai_summary_text = Column(String, nullable=True)
    summary_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
