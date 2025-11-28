from pydantic import BaseModel


class WeeklySummary(BaseModel):
    patient_id: str
    adherence_rate: float
    missed_doses: int
    flagged_symptoms: list[str]
    insights: list[str]
