from datetime import datetime
from pydantic import BaseModel


class DeviceEventLog(BaseModel):
    event_type: str
    payload: dict | None = None
    scheduled_time: datetime | None = None
    event_time: datetime | None = None
