from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func

from app.db.base import Base


class MedicationPlanItem(Base):
    __tablename__ = "medication_plan_items"

    id = Column(String, primary_key=True, index=True)
    medication_plan_id = Column(String, ForeignKey("medication_plans.id"), nullable=False, index=True)
    medication_id = Column(String, ForeignKey("medications.id"), nullable=True, index=True)
    custom_med_name = Column(String, nullable=True)
    dose_amount = Column(String, nullable=True)
    dose_unit = Column(String, nullable=True)
    frequency_pattern = Column(String, nullable=True)  # BID, TID, cron expression...
    slot_id = Column(String, nullable=True)
    time_of_day = Column(String, nullable=True)
    instructions = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
