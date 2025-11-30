from datetime import datetime
from pydantic import BaseModel, Field


class OverviewMetrics(BaseModel):
    patients: int
    adherence_rate: float
    emergency_signals_week: int
    ai_insights: int


class TrendPoint(BaseModel):
    label: str
    value: float


class AlertItem(BaseModel):
    message: str
    level: str
    time: datetime | None = None


class DoctorOverview(BaseModel):
    metrics: OverviewMetrics
    adherence_trend: list[TrendPoint]
    symptom_frequency: list[TrendPoint]
    alerts: list[AlertItem]
    adherence_summary: "AdherenceSummary"
    on_time_summary: "AdherenceSummary"
    missed_summary: "MissedSummary"
    symptom_population: "SymptomPopulation"
    severity_population: "SeverityPopulation"
    new_symptoms_population: "NewSymptomPopulation"
    symptom_by_patient: "SymptomByPatientChart"
    ai_notifications: list["AINotification"]


class PatientProfileCard(BaseModel):
    id: str
    name: str
    age: int | None = None
    gender: str | None = None
    avatar_url: str | None = None
    medical_history: list[str] = Field(default_factory=list)
    current_medications: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    primary_complaint: str | None = None
    lifestyle_factors: list[str] = Field(default_factory=list)
    recent_tests: list[str] = Field(default_factory=list)
    treatment_plan: list[str] = Field(default_factory=list)


class PatientRow(BaseModel):
    id: str
    name: str
    adherence: float
    alerts: int
    last_update: datetime | None = None


class PatientList(BaseModel):
    patients: list[PatientRow]


class TimelinePoint(BaseModel):
    label: str
    adherence: float
    alerts: int


class PatientTimeline(BaseModel):
    patient_id: str
    points: list[TimelinePoint]


class AdherenceKPIs(BaseModel):
    horizon: str  # week | month
    overall_adherence_rate: float
    on_time_rate: float
    missed_doses: int


class SymptomTrending(BaseModel):
    symptom: str
    count: int


class SeverityTrend(BaseModel):
    change_pct: float
    direction: str  # up/down/flat


class SeverityBar(BaseModel):
    label: str
    normal: int
    warning: int
    alert: int


class NewSymptom(BaseModel):
    symptom: str
    first_seen: datetime


class SymptomKPIs(BaseModel):
    horizon: str  # week | month
    frequency: int
    trending: list[SymptomTrending]
    severity_trend: SeverityTrend
    severity_bars: list[SeverityBar]
    new_symptoms: list[NewSymptom]


class AdherenceSummary(BaseModel):
    mean: float
    high_count: int
    medium_count: int
    low_count: int


class MissedPatient(BaseModel):
    patient_id: str
    patient_name: str
    missed_7d: int


class MissedSummary(BaseModel):
    total_7d: int
    total_30d: int
    per_patient_week: float
    top_patients: list[MissedPatient]


class SymptomPopulation(BaseModel):
    total_7d: int
    total_30d: int
    top: list[SymptomTrending]


class SeverityPopulation(BaseModel):
    change_pct: float
    direction: str
    patients_up: int
    flagged_patients: int


class NewSymptomPopulation(BaseModel):
    events: int
    patient_count: int
    top: list[SymptomTrending]
    critical_patients: int


class SymptomPatientSeries(BaseModel):
    label: str
    values: list[int]


class SymptomByPatientChart(BaseModel):
    labels: list[str]
    series: list[SymptomPatientSeries]


class AINotification(BaseModel):
    patient_id: str
    patient_name: str
    summary: str
    detail: str


class EdgeMessage(BaseModel):
    id: str
    patient_id: str
    patient_name: str
    device_id: str | None = None
    speaker: str | None = None
    direction: str
    content: str
    intent: str | None = None
    created_at: datetime


class EdgeMessageCreate(BaseModel):
    patient_id: str | None = None
    device_id: str | None = None
    speaker: str | None = None
    direction: str
    content: str
    intent: str | None = None


class EdgeMessageList(BaseModel):
    patient_id: str
    patient_name: str
    messages: list[EdgeMessage]


class PatientDashboard(BaseModel):
    patient: PatientProfileCard
    adherence: AdherenceKPIs
    symptoms: SymptomKPIs


class MedicationDose(BaseModel):
    med_name: str
    dose: str
    time: datetime
    status: str
    symptom: str | None = None


class PatientMedicationPlan(BaseModel):
    patient_id: str
    patient_name: str
    doses: list[MedicationDose]
