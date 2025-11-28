from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class DoseEventLog(Base):
    __tablename__ = "dose_event_logs"

    id = Column(String, primary_key=True, index=True)
    dose_id = Column(String, ForeignKey("dose_occurrences.id"), nullable=False, index=True)
    device_id = Column(String, ForeignKey("devices.id"), nullable=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    payload = Column(JSONB, nullable=True)
    event_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
