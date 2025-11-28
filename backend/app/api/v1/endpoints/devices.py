from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.device import DeviceCreate, DeviceOut, DeviceSchedule

router = APIRouter()


@router.post("", response_model=DeviceOut)
def register_device(payload: DeviceCreate, db: Session = Depends(get_db)) -> DeviceOut:
    # TODO: persist device and generate device_key securely
    return DeviceOut(id="device-demo", name=payload.name, device_key="device-key-placeholder")


@router.get("/{device_id}/schedule", response_model=DeviceSchedule)
def get_schedule(device_id: str, db: Session = Depends(get_db)) -> DeviceSchedule:
    # TODO: query active schedule for this device
    if not device_id:
        raise HTTPException(status_code=404, detail="Device not found")
    return DeviceSchedule(device_id=device_id, medication_plan_version="v1", doses=[])
