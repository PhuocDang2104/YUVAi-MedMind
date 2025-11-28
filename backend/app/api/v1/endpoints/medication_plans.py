from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.medication_plan import MedicationPlanCreate, MedicationPlanOut

router = APIRouter()


@router.post("", response_model=MedicationPlanOut)
def create_plan(payload: MedicationPlanCreate, db: Session = Depends(get_db)) -> MedicationPlanOut:
    # TODO: persist plan, generate dose events, push schedule to device
    return MedicationPlanOut(id="plan-demo", patient_id=payload.patient_id, medications=payload.medications)
