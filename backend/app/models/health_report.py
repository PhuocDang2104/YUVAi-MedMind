from sqlalchemy import Column, Date, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class HealthReport(Base):
    __tablename__ = "health_reports"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    report_type = Column(String, nullable=False)  # DAILY/WEEKLY/MONTHLY
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)
    file_url = Column(String, nullable=True)
    report_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
