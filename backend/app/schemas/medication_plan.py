from pydantic import BaseModel


class Medication(BaseModel):
    med_name: str
    dosage: str
    schedule: list[str]
    notes: str | None = None


class MedicationPlanBase(BaseModel):
    patient_id: str
    medications: list[Medication]


class MedicationPlanCreate(MedicationPlanBase):
    pass


class MedicationPlanOut(MedicationPlanBase):
    id: str

    class Config:
        orm_mode = True
