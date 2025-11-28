from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class NotificationEvent(Base):
    __tablename__ = "notification_events"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=True, index=True)
    trigger_source = Column(String, nullable=False, index=True)  # MISSED_DOSE/EMERGENCY_SIGNAL/...
    related_dose_id = Column(String, ForeignKey("dose_occurrences.id"), nullable=True, index=True)
    related_alert_id = Column(String, ForeignKey("alert_logs.id"), nullable=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    data_payload = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
