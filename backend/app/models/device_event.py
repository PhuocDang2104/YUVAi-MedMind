from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class DeviceEvent(Base):
    __tablename__ = "device_events"

    id = Column(String, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)
    payload = Column(JSONB, nullable=True)
    related_dose_id = Column(String, ForeignKey("dose_occurrences.id"), nullable=True, index=True)
    event_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
