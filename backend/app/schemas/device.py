from datetime import datetime
from pydantic import BaseModel


class DeviceBase(BaseModel):
    name: str


class DeviceCreate(DeviceBase):
    owner_id: str | None = None


class DeviceOut(DeviceBase):
    id: str
    device_key: str

    class Config:
        orm_mode = True


class DoseSchedule(BaseModel):
    slot_id: str
    med_name: str
    dosage: str
    scheduled_time: datetime


class DeviceSchedule(BaseModel):
    device_id: str
    medication_plan_version: str
    doses: list[DoseSchedule]
