from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base


class DoseOccurrence(Base):
    __tablename__ = "dose_occurrences"

    id = Column(String, primary_key=True, index=True)
    medication_plan_id = Column(String, ForeignKey("medication_plans.id"), nullable=False, index=True)
    plan_item_id = Column(String, ForeignKey("medication_plan_items.id"), nullable=False, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    device_id = Column(String, ForeignKey("devices.id"), nullable=True, index=True)
    slot_id = Column(String, nullable=True)
    scheduled_time = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(String, nullable=False, default="SCHEDULED", index=True)
    actual_time = Column(DateTime(timezone=True), nullable=True)
    snooze_count = Column(Integer, default=0, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
