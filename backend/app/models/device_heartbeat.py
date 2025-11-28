from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class DeviceHeartbeat(Base):
    __tablename__ = "device_heartbeats"

    id = Column(String, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False, index=True)
    battery = Column(String, nullable=True)
    temperature = Column(String, nullable=True)
    firmware_version = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    payload = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
