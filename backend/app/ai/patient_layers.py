from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.ai.gateway import AIGateway
from app.models import (
    DoseOccurrence,
    Medication,
    MedicationPlan,
    MedicationPlanItem,
    Patient,
    PatientProfile,
    SymptomLog,
)

DEFAULT_PATIENT_NAME = "Asha Pillai"

DEFAULT_SIDE_EFFECTS = {
    "Amlodipine": ["dizziness", "swelling", "flushing"],
    "Atorvastatin": ["muscle pain", "fatigue"],
    "Nitroglycerin": ["headache", "dizziness", "low blood pressure"],
    "Beta blocker": ["fatigue", "cold hands", "slow heart rate"],
}


def _calculate_age(dob) -> int | None:
    if not dob:
        return None
    today = datetime.now().date()
    return today.year - dob.year - (1 if (today.month, today.day) < (dob.month, dob.day) else 0)


def _get_patient(db: Session, patient_id: str | None) -> Patient:
    if patient_id:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    patient = db.query(Patient).filter(func.lower(Patient.full_name) == DEFAULT_PATIENT_NAME.lower()).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Default patient not found")
    return patient


def _recent_symptom_logs(db: Session, patient_id: str, limit: int = 8) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(hours=36)
    logs = (
        db.query(SymptomLog)
        .filter(SymptomLog.patient_id == patient_id)
        .filter(SymptomLog.created_at >= window_start)
        .order_by(SymptomLog.created_at.desc())
        .limit(limit)
        .all()
    )
    if not logs:
        logs = (
            db.query(SymptomLog)
            .filter(SymptomLog.patient_id == patient_id)
            .order_by(SymptomLog.created_at.desc())
            .limit(limit)
            .all()
        )
    formatted: list[dict[str, Any]] = []
    for log in logs:
        time_str = log.created_at.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")
        symptom_text = log.symptoms_raw or ""
        if not symptom_text and isinstance(log.structured_json, dict):
            vals = log.structured_json.get("symptoms") or []
            if isinstance(vals, list):
                symptom_text = ", ".join(vals)
            elif isinstance(vals, str):
                symptom_text = vals
        formatted.append(
            {
                "time": time_str,
                "symptom": symptom_text,
                "severity": log.severity or "unknown",
            }
        )
    return formatted


def _medication_snapshot(db: Session, patient_id: str) -> list[dict[str, Any]]:
    plan = (
        db.query(MedicationPlan)
        .filter(MedicationPlan.patient_id == patient_id, MedicationPlan.is_active == True)  # noqa: E712
        .order_by(MedicationPlan.created_at.desc())
        .first()
    )
    if not plan:
        return []
    items: list[MedicationPlanItem] = (
        db.query(MedicationPlanItem).filter(MedicationPlanItem.medication_plan_id == plan.id).all()
    )
    med_ids = [it.medication_id for it in items if it.medication_id]
    med_lookup = {}
    if med_ids:
        med_lookup = {m.id: m.name for m in db.query(Medication).filter(Medication.id.in_(med_ids)).all()}
    snapshot: list[dict[str, Any]] = []
    for item in items:
        name = item.custom_med_name or med_lookup.get(item.medication_id, "Unknown medication")
        side_effects = DEFAULT_SIDE_EFFECTS.get(name) or DEFAULT_SIDE_EFFECTS.get(name.split()[0], [])
        snapshot.append(
            {
                "name": name,
                "dose": " ".join(filter(None, [item.dose_amount, item.dose_unit])),
                "time_of_day": item.time_of_day or item.slot_id,
                "frequency": item.frequency_pattern,
                "instructions": item.instructions,
                "side_effects": side_effects,
            }
        )
    return snapshot


def _adherence_snapshot(db: Session, patient_id: str, days: int = 7) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    occurs = (
        db.query(DoseOccurrence)
        .filter(DoseOccurrence.patient_id == patient_id)
        .filter(DoseOccurrence.scheduled_time >= now - timedelta(days=days))
        .all()
    )
    total = len(occurs)
    on_time = sum(1 for o in occurs if o.status == "ON_TIME")
    late = sum(1 for o in occurs if o.status == "LATE")
    missed = sum(1 for o in occurs if o.status == "MISSED")
    adherence = round((on_time + late) / total * 100, 2) if total else 0.0
    return {
        "horizon_days": days,
        "total": total,
        "on_time": on_time,
        "late": late,
        "missed": missed,
        "adherence_pct": adherence,
    }


def _patient_profile(db: Session, patient_id: str) -> dict[str, Any]:
    profile = db.query(PatientProfile).filter(PatientProfile.patient_id == patient_id).first()
    if not profile:
        return {}
    return {
        "medical_history": profile.medical_history,
        "allergies": profile.allergies,
        "primary_complaint": profile.primary_complaint,
        "current_medications": profile.current_medications or [],
        "lifestyle_factors": profile.lifestyle_factors or [],
        "recent_tests": profile.recent_tests or [],
        "treatment_plan": profile.treatment_plan or [],
    }


def _build_layer1_prompt(patient: Patient, age: int | None, logs: list[dict[str, Any]], meds: list[dict[str, Any]]) -> str:
    history = patient.notes or "Không có ghi chú"
    meds_text = ", ".join({m["name"] for m in meds}) or "Chưa ghi nhận thuốc"
    logs_json = json.dumps(logs, ensure_ascii=False)
    return (
        f"Tóm tắt nhật ký triệu chứng cho bệnh nhân {patient.full_name} (tuổi: {age or 'N/A'}, tiền sử: {history}).\n"
        f"Dữ liệu 24-48h gần nhất: {logs_json}\n"
        "Trả về JSON với các field: "
        "physical_summary (list {time, symptom, severity}), "
        "mental_note (text nếu có cảm xúc/tâm trạng), "
        "warning_flag (true nếu đau ngực/khó thở/ngất/miss liều/triệu chứng nặng, else false), "
        "narrative (đoạn <=80 từ tiếng Việt, giọng bác sĩ, không bullet).\n"
        f"Thuốc đang dùng: {meds_text}. Nếu thiếu dữ liệu, vẫn phải trả JSON đủ key."
    )


def _build_layer2_prompt(
    patient: Patient,
    age: int | None,
    report: dict[str, Any],
    narrative: str,
    medical_records: dict[str, Any],
    adherence: dict[str, Any],
) -> str:
    report_json = json.dumps(report, ensure_ascii=False)
    med_json = json.dumps(medical_records, ensure_ascii=False)
    adherence_json = json.dumps(adherence, ensure_ascii=False)
    warning_flag = report.get("warning_flag", False)
    return (
        f"You advise a clinician about patient {patient.full_name} (age: {age or 'N/A'}). Refer to the patient in 3rd person, not 'you'.\n"
        f"Daily report JSON: {report_json}\n"
        f"Narrative summary: {narrative}\n"
        f"Medical record & meds: {med_json}\n"
        f"Adherence last 7 days: {adherence_json}\n"
        f"warning_flag: {warning_flag}\n"
        "Write one short paragraph (<=110 words, English, clinical tone). Structure: status recap (3rd person), 2-3 clear actions the clinician should advise, escalation if warning_flag or chest pain/shortness of breath/syncope.\n"
        "No bullets, no questions, no markdown. Respond in English only."
    )


def _parse_structured_report(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except Exception:
        return {"narrative": cleaned}


def _build_medical_records(patient: Patient, profile: dict[str, Any], meds: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "patient_id": patient.id,
        "condition": profile.get("primary_complaint") or profile.get("medical_history") or patient.notes,
        "medications": meds,
        "allergies": profile.get("allergies"),
        "lifestyle_factors": profile.get("lifestyle_factors", []),
    }


def _fallback_layer1(patient: Patient, logs: list[dict[str, Any]]) -> dict[str, Any]:
    top_logs = logs[:3]
    warning_terms = {"chest pain", "shortness of breath", "syncope", "faint", "collapse"}
    warning = False
    for l in top_logs:
        text = (l.get("symptom", "") or "").lower()
        if any(term in text for term in warning_terms):
            warning = True
        if (l.get("severity") or "").lower() in {"severe", "high"}:
            warning = True
    summary_bits = [f"{l.get('time')}: {l.get('symptom')}" for l in top_logs if l.get("symptom")]
    narrative = "AI not reachable. Quick summary: " + ("; ".join(summary_bits) if summary_bits else "No recent logs.")
    return {
        "physical_summary": top_logs,
        "mental_note": None,
        "warning_flag": warning,
        "narrative": narrative,
    }


def _fallback_layer2(patient: Patient, layer1: dict[str, Any], adherence: dict[str, Any]) -> str:
    adherence_pct = adherence.get("adherence_pct", 0)
    quick_summary = layer1.get("narrative", "")
    parts = [
        f"AI not reachable. Quick clinician note for {patient.full_name}:",
        f"- Summary: {quick_summary}",
        f"- 7d adherence: {adherence_pct}% (on-time + late).",
        "- Advise on-time dosing, hydration, monitor dizziness/shortness of breath.",
    ]
    if layer1.get("warning_flag"):
        parts.append("- Warning signs present; advise immediate clinical follow-up or escalation.")
    return "\n".join(parts)


async def generate_layer1_summary(db: Session, patient_id: str | None = None, gateway: AIGateway | None = None) -> dict[str, Any]:
    patient = _get_patient(db, patient_id)
    age = _calculate_age(patient.dob)
    logs = _recent_symptom_logs(db, patient.id)
    meds = _medication_snapshot(db, patient.id)
    profile = _patient_profile(db, patient.id)
    prompt = _build_layer1_prompt(patient, age, logs, meds)
    gw = gateway or AIGateway()
    owns_gateway = gateway is None
    try:
        result = await gw.run_inference(mode="layer1_summary", user_message=prompt, meta={"patient_id": patient.id})
    except Exception as exc:  # pragma: no cover - network path
        logging.error("Layer1 AI failed, using fallback: %s", exc)
        fallback = _fallback_layer1(patient, logs)
        narrative = fallback.get("narrative", "")
        warning_flag = fallback.get("warning_flag", False)
        if "narrative" in fallback:
            del fallback["narrative"]
        return {
            "layer": 1,
            "patient_id": patient.id,
            "patient_name": patient.full_name,
            "report": fallback,
            "narrative": narrative,
            "warning_flag": warning_flag,
            "context": {
                "logs": logs,
                "medications": meds,
                "profile": profile,
                "source": "fallback",
            },
        }
    finally:
        if owns_gateway:
            await gw.aclose()
    report = _parse_structured_report(result.content)
    narrative = report.get("narrative") or report.get("summary") or report.get("text") or result.content
    warning_flag = bool(report.get("warning_flag", False))
    if "narrative" in report:
        del report["narrative"]
    return {
        "layer": 1,
        "patient_id": patient.id,
        "patient_name": patient.full_name,
        "report": report,
        "narrative": narrative,
        "warning_flag": warning_flag,
        "context": {
            "logs": logs,
            "medications": meds,
            "profile": profile,
        },
    }


async def generate_layer2_suggestion(db: Session, patient_id: str | None = None, gateway: AIGateway | None = None) -> dict[str, Any]:
    gw = gateway or AIGateway()
    owns_gateway = gateway is None
    layer1 = await generate_layer1_summary(db, patient_id=patient_id, gateway=gw)
    patient = _get_patient(db, patient_id)
    age = _calculate_age(patient.dob)
    profile = layer1["context"]["profile"]
    meds = layer1["context"]["medications"]
    medical_records = _build_medical_records(patient, profile, meds)
    adherence = _adherence_snapshot(db, patient.id)
    prompt = _build_layer2_prompt(
        patient=patient,
        age=age,
        report=layer1["report"],
        narrative=layer1["narrative"],
        medical_records=medical_records,
        adherence=adherence,
    )
    try:
        result = await gw.run_inference(
            mode="layer2_suggestion",
            user_message=prompt,
            meta={"patient_id": patient.id, "warning_flag": layer1.get("warning_flag")},
        )
    except Exception as exc:  # pragma: no cover - network path
        logging.error("Layer2 AI failed, using fallback: %s", exc)
        suggestion = _fallback_layer2(patient, layer1, adherence)
        return {
            "layer": 2,
            "patient_id": patient.id,
            "patient_name": patient.full_name,
            "message": suggestion,
            "report": layer1["report"],
            "narrative": layer1["narrative"],
            "warning_flag": layer1.get("warning_flag"),
            "context": {
                "medical_records": medical_records,
                "adherence": adherence,
                "source": "fallback",
            },
        }
    finally:
        if owns_gateway:
            await gw.aclose()

    suggestion = result.content.strip()
    return {
        "layer": 2,
        "patient_id": patient.id,
        "patient_name": patient.full_name,
        "message": suggestion,
        "report": layer1["report"],
        "narrative": layer1["narrative"],
        "warning_flag": layer1.get("warning_flag"),
        "context": {
            "medical_records": medical_records,
            "adherence": adherence,
        },
    }
