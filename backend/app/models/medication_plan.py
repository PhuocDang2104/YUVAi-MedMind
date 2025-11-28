from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String
from sqlalchemy.sql import func

from app.db.base import Base


class MedicationPlan(Base):
    __tablename__ = "medication_plans"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=True, index=True)
    caregiver_id = Column(String, ForeignKey("caregivers.id"), nullable=True, index=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
