from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func

from app.db.base import Base


class EdgeTextLog(Base):
    __tablename__ = "edge_text_logs"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    device_id = Column(String, ForeignKey("devices.id"), nullable=True, index=True)
    speaker = Column(String, nullable=True)
    direction = Column(String, nullable=False)  # IN (edge->server) or OUT (server->edge)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
