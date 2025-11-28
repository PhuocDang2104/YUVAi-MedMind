from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.summary import WeeklySummary

router = APIRouter()


@router.get("/weekly/{patient_id}", response_model=WeeklySummary)
def get_weekly_summary(patient_id: str, db: Session = Depends(get_db)) -> WeeklySummary:
    # TODO: query analytics table populated by batch jobs / cloud LLM insights
    return WeeklySummary(
        patient_id=patient_id,
        adherence_rate=0.0,
        missed_doses=0,
        flagged_symptoms=[],
        insights=[],
    )
