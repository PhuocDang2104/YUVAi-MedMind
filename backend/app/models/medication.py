from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from app.db.base import Base


class Medication(Base):
    __tablename__ = "medications"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    generic_name = Column(String, nullable=True)
    form = Column(String, nullable=True)
    route = Column(String, nullable=True)
    strength = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
