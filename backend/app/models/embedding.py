from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, REAL
from sqlalchemy.sql import func

from app.db.base import Base


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(String, primary_key=True, index=True)
    object_type = Column(String, nullable=False, index=True)  # INTERACTION/SYMPTOM_LOG/INSIGHT/...
    object_id = Column(String, nullable=False, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=True, index=True)
    embedding = Column(ARRAY(REAL), nullable=False)
    meta = Column("metadata", JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
