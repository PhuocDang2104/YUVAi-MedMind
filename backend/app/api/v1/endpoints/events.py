from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.event import DeviceEventLog

router = APIRouter()


@router.post("")
def ingest_event(device_id: str, payload: DeviceEventLog, db: Session = Depends(get_db)) -> dict[str, str]:
    # TODO: persist event with status and timestamps
    return {"status": "accepted", "device_id": device_id, "event_type": payload.event_type}


@router.post("/sync")
def sync_events(device_id: str, payload: list[DeviceEventLog], db: Session = Depends(get_db)) -> dict[str, int]:
    # TODO: bulk insert events
    return {"synced": len(payload)}
