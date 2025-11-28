from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base


class NotificationDelivery(Base):
    __tablename__ = "notification_deliveries"

    id = Column(String, primary_key=True, index=True)
    notification_event_id = Column(String, ForeignKey("notification_events.id"), nullable=False, index=True)
    channel_id = Column(String, ForeignKey("notification_channels.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="PENDING", index=True)
    send_attempts = Column(Integer, default=0, nullable=False)
    last_error = Column(String, nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
