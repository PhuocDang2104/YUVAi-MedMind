from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class PatientProfile(Base):
    __tablename__ = "patient_profiles"
    __table_args__ = (UniqueConstraint("patient_id", name="uq_patient_profile_patient"),)

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    avatar_url = Column(String, nullable=True)
    medical_history = Column(String, nullable=True)
    allergies = Column(String, nullable=True)
    primary_complaint = Column(String, nullable=True)
    current_medications = Column(JSONB, nullable=True)
    lifestyle_factors = Column(JSONB, nullable=True)
    recent_tests = Column(JSONB, nullable=True)
    treatment_plan = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
