from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func

from app.db.base import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True)
    device_uid = Column(String, nullable=False, unique=True, index=True)
    device_key_hash = Column(String, nullable=False)
    firmware_version = Column(String, nullable=True)
    status = Column(String, nullable=False, default="UNPAIRED")
    paired_patient_id = Column(String, ForeignKey("patients.id"), nullable=True, index=True)
    last_heartbeat_at = Column(DateTime(timezone=True), nullable=True)
    last_ip = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
