from collections import Counter
from datetime import date, datetime, timedelta, timezone
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import (
    AlertLog,
    Device,
    DeviceEvent,
    DoseEventLog,
    DoseOccurrence,
    Medication,
    MedicationPlan,
    MedicationPlanItem,
    Patient,
    PatientProfile,
    SymptomLog,
    EdgeTextLog,
)
from app.schemas.doctor import (
    AlertItem,
    AdherenceKPIs,
    AdherenceSummary,
    AINotification,
    DoctorOverview,
    MedicationDose,
    MissedPatient,
    MissedSummary,
    NewSymptom,
    NewSymptomPopulation,
    OverviewMetrics,
    PatientList,
    PatientDashboard,
    PatientMedicationPlan,
    PatientProfileCard,
    PatientRow,
    PatientTimeline,
    EdgeMessage,
    EdgeMessageCreate,
    EdgeMessageList,
    SeverityBar,
    SeverityPopulation,
    SeverityTrend,
    SymptomByPatientChart,
    SymptomKPIs,
    SymptomPatientSeries,
    SymptomPopulation,
    SymptomTrending,
    TimelinePoint,
    TrendPoint,
)

router = APIRouter()

ANALYTICS_PATIENT_NAME = "Asha Pillai"
ALLOWED_PATIENT_NAMES = {"Asha Pillai", "Emily Brown", "John Carter"}

def _allowed_patient_ids(db: Session) -> list[str]:
    return [p.id for p in db.query(Patient.id).filter(Patient.full_name.in_(ALLOWED_PATIENT_NAMES)).all()]


def _adherence_from_occurrences(occurs: list[DoseOccurrence], include_late: bool = True) -> float:
    if not occurs:
        return 0.0
    taken_status = {"ON_TIME", "LATE"} if include_late else {"ON_TIME"}
    taken = sum(1 for o in occurs if o.status in taken_status)
    return round(taken / len(occurs) * 100, 2)


def _calculate_age(dob: date | None) -> int | None:
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - (1 if (today.month, today.day) < (dob.month, dob.day) else 0)


def _list_from_value(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    if isinstance(value, str):
        parts = value.replace(";", ",").split(",")
        return [p.strip() for p in parts if p.strip()]
    return []


def _extract_symptom_terms(log: SymptomLog) -> list[str]:
    terms: list[str] = []
    structured = log.structured_json or {}
    if isinstance(structured, dict):
        for key in ("symptoms", "symptom"):
            val = structured.get(key)
            if isinstance(val, list):
                terms.extend([str(v) for v in val])
            elif isinstance(val, str):
                parts = val.replace(";", ",").split(",")
                terms.extend([p.strip() for p in parts if p.strip()])
    if not terms and log.symptoms_raw:
        terms.extend([part.strip() for part in log.symptoms_raw.replace(" and ", ",").split(",") if part.strip()])
    clean: list[str] = []
    for t in terms:
        normalized = " ".join(t.lower().split())
        if normalized:
            clean.append(normalized)
    return clean


def _severity_score(log: SymptomLog) -> float:
    if not log.severity:
        return 0.0
    mapping = {"mild": 1.0, "low": 1.0, "moderate": 2.0, "medium": 2.0, "severe": 3.0, "high": 3.0}
    return mapping.get(log.severity.lower(), 0.0)


def _avg_severity(logs: list[SymptomLog]) -> float:
    scores = [score for score in (_severity_score(l) for l in logs) if score > 0]
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)


def _severity_bucket(log: SymptomLog) -> str:
    sev = (log.severity or "").lower()
    if sev in {"severe", "high"}:
        return "alert"
    if sev in {"moderate", "medium"}:
        return "warning"
    return "normal"


def _get_patient_or_default(db: Session, patient_id: str | None) -> Patient:
    if patient_id:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        if patient.full_name not in ALLOWED_PATIENT_NAMES:
            raise HTTPException(status_code=404, detail="Patient not allowed")
        return patient
    patient = db.query(Patient).filter(func.lower(Patient.full_name) == ANALYTICS_PATIENT_NAME.lower()).first()
    if patient:
        return patient
    patient = db.query(Patient).filter(Patient.full_name.in_(ALLOWED_PATIENT_NAMES)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="No patients available")
    return patient


def _ensure_device(db: Session, device_id: str | None, patient_id: str) -> str | None:
    """Return a valid device_id, creating a placeholder if a custom id is given but missing."""
    if not device_id:
        return None
    device = db.query(Device).filter(Device.id == device_id).first()
    if device:
        if device.paired_patient_id != patient_id:
            device.paired_patient_id = patient_id
        return device.id
    placeholder = Device(
        id=device_id,
        device_uid=device_id,
        device_key_hash="placeholder",
        firmware_version="1.0.0",
        status="PAIRED",
        paired_patient_id=patient_id,
        last_ip="0.0.0.0",
    )
    db.add(placeholder)
    db.flush()
    return placeholder.id


@router.get("/overview", response_model=DoctorOverview)
def doctor_overview(db: Session = Depends(get_db)) -> DoctorOverview:
    allowed_ids = _allowed_patient_ids(db)
    patients = db.query(Patient).filter(Patient.id.in_(allowed_ids)).all()
    occurrences = db.query(DoseOccurrence).filter(DoseOccurrence.patient_id.in_(allowed_ids)).all()
    now = datetime.now(timezone.utc)
    alerts_count = (
        db.query(AlertLog)
        .filter(AlertLog.patient_id.in_(allowed_ids))
        .filter(AlertLog.created_at >= now - timedelta(days=7))
        .count()
    )
    metrics = OverviewMetrics(
        patients=len(patients),
        adherence_rate=_adherence_from_occurrences(occurrences),
        emergency_signals_week=alerts_count,
        ai_insights=6,
    )

    # Build simple trend by day over last 7 entries
    points: list[TrendPoint] = []
    grouped = (
        db.query(
            func.date(DoseOccurrence.scheduled_time),
            func.count(DoseOccurrence.id),
            func.sum(case((DoseOccurrence.status == "ON_TIME", 1), else_=0)),
        )
        .filter(DoseOccurrence.patient_id.in_(allowed_ids))
        .group_by(func.date(DoseOccurrence.scheduled_time))
        .order_by(func.date(DoseOccurrence.scheduled_time).desc())
        .limit(7)
        .all()
    )
    for day, total, on_time in reversed(grouped):
        rate = round((on_time or 0) / (total or 1) * 100, 2)
        points.append(TrendPoint(label=str(day), value=rate))

    symptom_freq: list[TrendPoint] = []
    sym_group = (
        db.query(func.date(SymptomLog.created_at), func.count(SymptomLog.id))
        .filter(SymptomLog.patient_id.in_(allowed_ids))
        .group_by(func.date(SymptomLog.created_at))
        .order_by(func.date(SymptomLog.created_at).desc())
        .limit(7)
        .all()
    )
    for day, cnt in reversed(sym_group):
        symptom_freq.append(TrendPoint(label=str(day), value=cnt))

    alert_items: list[AlertItem] = []
    alert_rows = (
        db.query(AlertLog)
        .filter(AlertLog.patient_id.in_(allowed_ids))
        .order_by(AlertLog.created_at.desc())
        .limit(5)
        .all()
    )
    for a in alert_rows:
        alert_items.append(AlertItem(message=a.symptoms or "Alert", level=a.risk_level or "HIGH", time=a.created_at))

    # Adherence summaries
    adherence_per_patient: dict[str, float] = {}
    on_time_per_patient: dict[str, float] = {}
    for p in patients:
        p_occurs = [o for o in occurrences if o.patient_id == p.id]
        adherence_per_patient[p.id] = _adherence_from_occurrences(p_occurs, include_late=True)
        on_time_per_patient[p.id] = _adherence_from_occurrences(p_occurs, include_late=False)
    adherence_values = list(adherence_per_patient.values()) or [0]
    on_time_values = list(on_time_per_patient.values()) or [0]
    adherence_summary = AdherenceSummary(
        mean=round(sum(adherence_values) / len(adherence_values), 2),
        high_count=sum(1 for v in adherence_values if v > 90),
        medium_count=sum(1 for v in adherence_values if 70 <= v <= 90),
        low_count=sum(1 for v in adherence_values if v < 70),
    )
    on_time_summary = AdherenceSummary(
        mean=round(sum(on_time_values) / len(on_time_values), 2),
        high_count=sum(1 for v in on_time_values if v > 90),
        medium_count=sum(1 for v in on_time_values if 70 <= v <= 90),
        low_count=sum(1 for v in on_time_values if v < 70),
    )

    # Missed doses
    missed_7d_total = (
        db.query(DoseOccurrence)
        .filter(DoseOccurrence.patient_id.in_(allowed_ids))
        .filter(DoseOccurrence.status == "MISSED")
        .filter(DoseOccurrence.scheduled_time >= now - timedelta(days=7))
        .count()
    )
    missed_30d_total = (
        db.query(DoseOccurrence)
        .filter(DoseOccurrence.patient_id.in_(allowed_ids))
        .filter(DoseOccurrence.status == "MISSED")
        .filter(DoseOccurrence.scheduled_time >= now - timedelta(days=30))
        .count()
    )
    per_patient_week = round(missed_7d_total / max(1, len(patients)), 2)
    top_patients: list[MissedPatient] = []
    for p in patients:
        missed_p = (
            db.query(DoseOccurrence)
            .filter(DoseOccurrence.patient_id == p.id, DoseOccurrence.status == "MISSED")
            .filter(DoseOccurrence.scheduled_time >= now - timedelta(days=7))
            .count()
        )
        if missed_p > 0:
            top_patients.append(MissedPatient(patient_id=p.id, patient_name=p.full_name, missed_7d=missed_p))
    top_patients = sorted(top_patients, key=lambda x: x.missed_7d, reverse=True)[:3]
    missed_summary = MissedSummary(total_7d=missed_7d_total, total_30d=missed_30d_total, per_patient_week=per_patient_week, top_patients=top_patients)

    # Symptom population
    symptoms_7d = (
        db.query(SymptomLog)
        .filter(SymptomLog.patient_id.in_(allowed_ids))
        .filter(SymptomLog.created_at >= now - timedelta(days=7))
        .all()
    )
    symptoms_30d = (
        db.query(SymptomLog)
        .filter(SymptomLog.patient_id.in_(allowed_ids))
        .filter(SymptomLog.created_at >= now - timedelta(days=30))
        .all()
    )
    sym_counter = Counter()
    for s in symptoms_7d:
        for term in _extract_symptom_terms(s):
            sym_counter[term] += 1
    top_symptoms = [SymptomTrending(symptom=term.title(), count=count) for term, count in sym_counter.most_common(3)]
    symptom_population = SymptomPopulation(total_7d=len(symptoms_7d), total_30d=len(symptoms_30d), top=top_symptoms)

    # Severity population
    def _avg_for_patient(logs: list[SymptomLog], pid: str) -> float:
        return _avg_severity([l for l in logs if l.patient_id == pid])

    symptoms_prev = (
        db.query(SymptomLog)
        .filter(SymptomLog.patient_id.in_(allowed_ids))
        .filter(SymptomLog.created_at < now - timedelta(days=7))
        .filter(SymptomLog.created_at >= now - timedelta(days=14))
        .all()
    )
    avg_current = _avg_severity(symptoms_7d)
    avg_prev = _avg_severity(symptoms_prev)
    change_pct = 0.0
    direction = "flat"
    if avg_prev > 0:
        change_pct = round((avg_current - avg_prev) / avg_prev * 100, 2)
    elif avg_current > 0:
        change_pct = 100.0
    if change_pct > 2:
        direction = "up"
    elif change_pct < -2:
        direction = "down"
    patients_up = sum(1 for p in patients if _avg_for_patient(symptoms_7d, p.id) > _avg_for_patient(symptoms_prev, p.id))
    flagged_patients = sum(1 for s in symptoms_7d if (s.severity or "").lower() in {"severe", "high"})
    severity_population = SeverityPopulation(change_pct=change_pct, direction=direction, patients_up=patients_up, flagged_patients=flagged_patients)

    # New symptoms (population)
    first_seen: dict[str, datetime] = {}
    for log in db.query(SymptomLog).filter(SymptomLog.patient_id.in_(allowed_ids)).order_by(SymptomLog.created_at.asc()).all():
        for term in _extract_symptom_terms(log):
            if term not in first_seen:
                first_seen[term] = log.created_at or now
    new_events = {term: ts for term, ts in first_seen.items() if ts and ts >= now - timedelta(days=7)}
    new_count = len(new_events)
    new_symptom_top = Counter()
    patient_new: set[str] = set()
    for log in symptoms_7d:
        for term in _extract_symptom_terms(log):
            if term in new_events:
                new_symptom_top[term] += 1
                patient_new.add(log.patient_id)
    new_top = [SymptomTrending(symptom=term.title(), count=count) for term, count in new_symptom_top.most_common(3)]
    critical_patients = len({log.patient_id for log in symptoms_7d if (log.severity or "").lower() in {"severe", "high"}})
    new_symptoms_population = NewSymptomPopulation(events=new_count, patient_count=len(patient_new), top=new_top, critical_patients=critical_patients)

    # Symptom by patient (stacked by patient, grouped per day)
    labels: list[str] = []
    series: list[SymptomPatientSeries] = []
    day_labels: list[str] = []
    for i in range(6, -1, -1):
        day_labels.append((now - timedelta(days=i)).strftime("%a"))
    labels = day_labels
    counts_by_patient: dict[str, list[int]] = {p.id: [0] * len(labels) for p in patients}
    for log in symptoms_7d:
        for idx, lbl in enumerate(labels):
            day_date = (now - timedelta(days=6 - idx)).date()
            if log.created_at and log.created_at.date() == day_date and log.patient_id in counts_by_patient:
                counts_by_patient[log.patient_id][idx] += 1
    for p in patients:
        series.append(SymptomPatientSeries(label=p.full_name, values=counts_by_patient[p.id]))
    symptom_by_patient = SymptomByPatientChart(labels=labels, series=series)

    ai_notifications: list[AINotification] = []
    for p in patients:
        adh = adherence_per_patient.get(p.id, 0)
        sym_ct = len([s for s in symptoms_7d if s.patient_id == p.id])
        summary = f"Adherence {adh}% | {sym_ct} symptoms this week"
        detail_map = {
            "Asha Pillai": "Stable BP control with occasional dizziness; monitor chest tightness after activity and hydrate.",
            "John Carter": "Adherence solid; mild headaches and lightheadedness reported; continue walks and avoid caffeine spikes.",
            "Emily Brown": "Lower adherence; shortness of breath and chest discomfort noted; reinforce timing and watch exertion."
        }
        detail = detail_map.get(p.full_name, "Monitoring adherence and recent symptoms; no critical alerts.")
        ai_notifications.append(AINotification(patient_id=p.id, patient_name=p.full_name, summary=summary, detail=detail))

    return DoctorOverview(
        metrics=metrics,
        adherence_trend=points,
        symptom_frequency=symptom_freq,
        alerts=alert_items,
        adherence_summary=adherence_summary,
        on_time_summary=on_time_summary,
        missed_summary=missed_summary,
        symptom_population=symptom_population,
        severity_population=severity_population,
        new_symptoms_population=new_symptoms_population,
        symptom_by_patient=symptom_by_patient,
        ai_notifications=ai_notifications,
    )


@router.get("/patients", response_model=PatientList)
def doctor_patients(db: Session = Depends(get_db)) -> PatientList:
    patients = db.query(Patient).filter(Patient.full_name.in_(ALLOWED_PATIENT_NAMES)).all()
    rows: list[PatientRow] = []
    for p in patients:
        occurs = db.query(DoseOccurrence).filter(DoseOccurrence.patient_id == p.id).all()
        adherence = _adherence_from_occurrences(occurs)
        alerts = db.query(AlertLog).filter(AlertLog.patient_id == p.id).count()
        last_update = db.query(DoseOccurrence).filter(DoseOccurrence.patient_id == p.id).order_by(DoseOccurrence.updated_at.desc()).first()
        rows.append(
            PatientRow(
                id=p.id,
                name=p.full_name,
                adherence=adherence,
                alerts=alerts,
                last_update=last_update.updated_at if last_update else None,
            )
        )
    return PatientList(patients=rows)


@router.get("/patients/{patient_id}/dashboard", response_model=PatientDashboard)
def patient_dashboard(patient_id: str, horizon: str = "week", db: Session = Depends(get_db)) -> PatientDashboard:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    profile_row = db.query(PatientProfile).filter(PatientProfile.patient_id == patient_id).first()

    horizon = (horizon or "week").lower()
    if horizon not in {"week", "month"}:
        raise HTTPException(status_code=400, detail="horizon must be 'week' or 'month'")
    days = 7 if horizon == "week" else 30
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(days=days)
    prev_window_start = window_start - timedelta(days=days)

    occurs = (
        db.query(DoseOccurrence)
        .filter(DoseOccurrence.patient_id == patient_id)
        .filter(DoseOccurrence.scheduled_time >= window_start)
        .all()
    )
    missed = (
        db.query(DoseOccurrence)
        .filter(DoseOccurrence.patient_id == patient_id)
        .filter(DoseOccurrence.status == "MISSED")
        .filter(DoseOccurrence.scheduled_time >= window_start)
        .count()
    )

    symptoms_window = (
        db.query(SymptomLog)
        .filter(SymptomLog.patient_id == patient_id)
        .filter(SymptomLog.created_at >= window_start)
        .order_by(SymptomLog.created_at.desc())
        .all()
    )
    prev_symptoms = (
        db.query(SymptomLog)
        .filter(SymptomLog.patient_id == patient_id)
        .filter(SymptomLog.created_at < window_start)
        .filter(SymptomLog.created_at >= prev_window_start)
        .all()
    )
    symptom_counter = Counter()
    for s in symptoms_window:
        for term in _extract_symptom_terms(s):
            symptom_counter[term] += 1
    trending = [SymptomTrending(symptom=term.title(), count=count) for term, count in symptom_counter.most_common(3)]

    avg_sev_current = _avg_severity(symptoms_window)
    avg_sev_prev = _avg_severity(prev_symptoms)
    change_pct = 0.0
    if avg_sev_prev > 0:
        change_pct = round((avg_sev_current - avg_sev_prev) / avg_sev_prev * 100, 1)
    elif avg_sev_current > 0:
        change_pct = 100.0
    direction = "flat"
    if change_pct > 2:
        direction = "up"
    elif change_pct < -2:
        direction = "down"

    all_symptoms = (
        db.query(SymptomLog)
        .filter(SymptomLog.patient_id == patient_id)
        .order_by(SymptomLog.created_at.asc())
        .all()
    )
    first_seen: dict[str, datetime | None] = {}
    for log in all_symptoms:
        for term in _extract_symptom_terms(log):
            if term not in first_seen:
                first_seen[term] = log.created_at or now
    new_symptoms = [
        NewSymptom(symptom=term.title(), first_seen=seen)
        for term, seen in first_seen.items()
        if seen and seen >= window_start
    ]
    new_symptoms = sorted(new_symptoms, key=lambda s: s.first_seen, reverse=True)[:7]

    # Build severity bars (stacked) based on horizon buckets
    bucket_count = 7 if horizon == "week" else 4
    bucket_length = timedelta(days=1) if horizon == "week" else timedelta(days=7)
    bars: list[SeverityBar] = []
    for idx in range(bucket_count):
        bucket_start = window_start + bucket_length * idx
        bucket_end = bucket_start + bucket_length
        label = bucket_start.strftime("%a") if horizon == "week" else f"Week {idx + 1}"
        normal = warning = alert = 0
        for log in symptoms_window:
            if not log.created_at:
                continue
            if bucket_start <= log.created_at < bucket_end:
                bucket = _severity_bucket(log)
                if bucket == "alert":
                    alert += 1
                elif bucket == "warning":
                    warning += 1
                else:
                    normal += 1
        bars.append(SeverityBar(label=label, normal=normal, warning=warning, alert=alert))

    profile_data = PatientProfileCard(
        id=patient.id,
        name=patient.full_name,
        age=_calculate_age(patient.dob),
        gender=patient.gender.title() if patient.gender else None,
        avatar_url=profile_row.avatar_url if profile_row else None,
        medical_history=_list_from_value(profile_row.medical_history if profile_row else None) or _list_from_value(patient.notes),
        current_medications=_list_from_value(profile_row.current_medications if profile_row else None),
        allergies=_list_from_value(profile_row.allergies if profile_row else None),
        primary_complaint=(profile_row.primary_complaint if profile_row else None) or patient.notes,
        lifestyle_factors=_list_from_value(profile_row.lifestyle_factors if profile_row else None),
        recent_tests=_list_from_value(profile_row.recent_tests if profile_row else None),
        treatment_plan=_list_from_value(profile_row.treatment_plan if profile_row else None),
    )
    adherence_metrics = AdherenceKPIs(
        horizon=horizon,
        overall_adherence_rate=_adherence_from_occurrences(occurs, include_late=True),
        on_time_rate=_adherence_from_occurrences(occurs, include_late=False),
        missed_doses=missed,
    )
    symptom_kpis = SymptomKPIs(
        horizon=horizon,
        frequency=len(symptoms_window),
        trending=trending,
        severity_trend=SeverityTrend(change_pct=change_pct, direction=direction),
        severity_bars=bars,
        new_symptoms=new_symptoms,
    )
    return PatientDashboard(patient=profile_data, adherence=adherence_metrics, symptoms=symptom_kpis)


@router.get("/symptom_analytics/messages", response_model=EdgeMessageList)
def list_edge_messages(patient_id: str | None = None, db: Session = Depends(get_db)) -> EdgeMessageList:
    patient = _get_patient_or_default(db, patient_id)
    messages: list[EdgeMessage] = []
    rows = (
        db.query(EdgeTextLog)
        .filter(EdgeTextLog.patient_id == patient.id)
        .order_by(EdgeTextLog.created_at.desc())
        .limit(50)
        .all()
    )
    for row in rows:
        messages.append(
            EdgeMessage(
                id=row.id,
                patient_id=patient.id,
                patient_name=patient.full_name,
                device_id=row.device_id,
                speaker=row.speaker,
                direction=row.direction,
                content=row.content,
                created_at=row.created_at,
            )
        )
    return EdgeMessageList(patient_id=patient.id, patient_name=patient.full_name, messages=messages)


@router.post("/symptom_analytics/messages", response_model=EdgeMessage)
def create_edge_message(payload: EdgeMessageCreate, db: Session = Depends(get_db)) -> EdgeMessage:
    patient = _get_patient_or_default(db, payload.patient_id)
    if payload.direction not in {"IN", "OUT"}:
        raise HTTPException(status_code=400, detail="direction must be IN or OUT")
    device_id = _ensure_device(db, payload.device_id, patient.id)
    new_id = str(uuid.uuid4())
    row = EdgeTextLog(
        id=new_id,
        patient_id=patient.id,
        device_id=device_id,
        speaker=payload.speaker,
        direction=payload.direction,
        content=payload.content,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return EdgeMessage(
        id=row.id,
        patient_id=patient.id,
        patient_name=patient.full_name,
        device_id=row.device_id,
        speaker=row.speaker,
        direction=row.direction,
        content=row.content,
        created_at=row.created_at,
    )


@router.delete("/symptom_analytics/messages")
def clear_edge_messages(patient_id: str | None = None, db: Session = Depends(get_db)) -> dict[str, int]:
    patient = _get_patient_or_default(db, patient_id)
    deleted = db.query(EdgeTextLog).filter(EdgeTextLog.patient_id == patient.id).delete(synchronize_session=False)
    db.commit()
    return {"deleted": deleted}


@router.get("/patients/{patient_id}/timeline", response_model=PatientTimeline)
def patient_timeline(patient_id: str, horizon: str = "day", db: Session = Depends(get_db)) -> PatientTimeline:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    horizon = (horizon or "day").lower()
    if horizon not in {"day", "hour"}:
        raise HTTPException(status_code=400, detail="horizon must be 'day' or 'hour'")
    now = datetime.now(timezone.utc)
    bucket_expr = func.date(DoseOccurrence.scheduled_time) if horizon == "day" else func.date_trunc("hour", DoseOccurrence.scheduled_time)
    points: list[TimelinePoint] = []
    grouped = (
        db.query(
            bucket_expr,
            func.count(DoseOccurrence.id),
            func.sum(case((DoseOccurrence.status == "ON_TIME", 1), else_=0)),
        )
        .filter(DoseOccurrence.patient_id == patient_id)
        .filter(DoseOccurrence.scheduled_time >= now - timedelta(days=7))
        .group_by(bucket_expr)
        .order_by(bucket_expr)
        .all()
    )
    for bucket, total, on_time in grouped:
        rate = round((on_time or 0) / (total or 1) * 100, 2)
        alert_q = db.query(AlertLog).filter(AlertLog.patient_id == patient_id)
        if horizon == "day":
            alert_q = alert_q.filter(func.date(AlertLog.created_at) == bucket)
            label = str(bucket)
        else:
            alert_q = alert_q.filter(func.date_trunc("hour", AlertLog.created_at) == bucket)
            label = bucket.strftime("%Y-%m-%d %H:00") if hasattr(bucket, "strftime") else str(bucket)
        alerts = alert_q.count()
        points.append(TimelinePoint(label=label, adherence=rate, alerts=alerts))
    return PatientTimeline(patient_id=patient_id, points=points)


@router.get("/patients/{patient_id}/medication_plan", response_model=PatientMedicationPlan)
def patient_medication_plan(patient_id: str, db: Session = Depends(get_db)) -> PatientMedicationPlan:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    plans = db.query(MedicationPlan).filter(MedicationPlan.patient_id == patient_id, MedicationPlan.is_active == True).all()  # noqa: E712
    if not plans:
        raise HTTPException(status_code=404, detail="No active medication plan found")
    plan_ids = [p.id for p in plans]

    occurs = (
        db.query(DoseOccurrence, Medication.name, MedicationPlanItem.dose_amount, MedicationPlanItem.dose_unit)
        .join(MedicationPlanItem, MedicationPlanItem.id == DoseOccurrence.plan_item_id)
        .join(Medication, Medication.id == MedicationPlanItem.medication_id)
        .filter(DoseOccurrence.patient_id == patient_id, DoseOccurrence.medication_plan_id.in_(plan_ids))
        .order_by(DoseOccurrence.scheduled_time.asc())
        .all()
    )
    doses: list[MedicationDose] = []
    for occ, med_name, dose_amount, dose_unit in occurs:
        symptom = (
            db.query(SymptomLog)
            .filter(SymptomLog.patient_id == patient_id)
            .order_by(SymptomLog.created_at.desc())
            .first()
        )
        dose_label = occ.slot_id or " ".join(filter(None, [dose_amount, dose_unit])).strip() or "1 viên"
        doses.append(
            MedicationDose(
                med_name=med_name or "Thuốc",
                dose=dose_label,
                time=occ.scheduled_time,
                status=occ.status,
                symptom=symptom.symptoms_raw if symptom else None,
            )
        )
    return PatientMedicationPlan(
        patient_id=patient.id,
        patient_name=patient.full_name,
        doses=doses,
    )
