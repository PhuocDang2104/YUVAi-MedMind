"""
Seed script for local development.
Creates richer English demo data: multiple patients, dense dose occurrences (hourly and daily), alerts, symptoms, and device activity.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import (
    AlertLog,
    Caregiver,
    Conversation,
    EdgeTextLog,
    Device,
    DeviceEvent,
    DeviceHeartbeat,
    DoseEventLog,
    DoseOccurrence,
    Doctor,
    InteractionLog,
    LLMRequest,
    Medication,
    MedicationPlan,
    MedicationPlanItem,
    MedicationQuestionLog,
    NotificationChannel,
    NotificationDelivery,
    NotificationEvent,
    Patient,
    PatientCaregiver,
    PatientDoctor,
    PatientProfile,
    SymptomLog,
    User,
    UserRole,
)


def _uuid() -> str:
    return str(uuid4())


def _set_statuses(occurs: list[DoseOccurrence], taken_ratio: float, on_time_ratio: float) -> None:
    if not occurs:
        return
    n = len(occurs)
    on_time_target = max(0, min(n, round(n * on_time_ratio)))
    taken_target = max(on_time_target, min(n, round(n * taken_ratio)))
    # Start all on time for a high baseline
    for occ in occurs:
        occ.status = "ON_TIME"
    late_needed = max(0, taken_target - on_time_target)
    missed_needed = max(0, n - taken_target)
    # Spread late doses evenly
    step_late = max(2, n // max(1, late_needed)) if late_needed else n + 1
    idx = 0
    while late_needed > 0 and idx < n:
        occurs[idx].status = "LATE"
        late_needed -= 1
        idx += step_late
    # Spread missed doses sparsely
    step_missed = max(3, n // max(1, missed_needed)) if missed_needed else n + 1
    idx = 1
    while missed_needed > 0 and idx < n:
        occurs[idx].status = "MISSED"
        missed_needed -= 1
        idx += step_missed


def get_or_create_user(session, email: str, role: UserRole, full_name: str) -> User:
    stmt = select(User).where(User.email == email)
    user = session.execute(stmt).scalar_one_or_none()
    if user:
        return user
    user = User(
        id=_uuid(),
        email=email,
        password_hash="hashed-password",
        full_name=full_name,
        role=role,
    )
    session.add(user)
    session.flush()
    return user


def add_dense_doses(
    session, plan: MedicationPlan, items: list[MedicationPlanItem], patient: Patient, device: Device | None, base_time: datetime
) -> list[DoseOccurrence]:
    """Generate a dense timeline: last 7 days with morning/noon/evening slots plus the last 24h hourly windows."""
    all_doses: list[DoseOccurrence] = []

    # Daily buckets for 7 days
    day_slots = [(8, "Morning"), (12, "Noon"), (20, "Evening")]
    status_cycle = ["ON_TIME", "LATE", "MISSED"]
    for day in range(7):
        day_time = base_time - timedelta(days=day)
        for idx, item in enumerate(items):
            hour, label = day_slots[idx % len(day_slots)]
            status = status_cycle[(day + idx) % len(status_cycle)]
            dose = DoseOccurrence(
                id=_uuid(),
                medication_plan_id=plan.id,
                plan_item_id=item.id,
                patient_id=patient.id,
                device_id=device.id if device else None,
                slot_id=item.slot_id,
                scheduled_time=day_time.replace(hour=hour, minute=0, second=0, microsecond=0),
                status=status,
                actual_time=day_time.replace(hour=hour, minute=15, second=0, microsecond=0) if status == "ON_TIME" else None,
                notes=f"{label} dose",
            )
            all_doses.append(dose)

    # Hourly window for last 24h (device focused)
    for h in range(24):
        scheduled = base_time - timedelta(hours=h)
        status = "ON_TIME" if h % 3 == 0 else ("LATE" if h % 3 == 1 else "MISSED")
        dose = DoseOccurrence(
            id=_uuid(),
            medication_plan_id=plan.id,
            plan_item_id=items[0].id,
            patient_id=patient.id,
            device_id=device.id if device else None,
            slot_id=items[0].slot_id,
            scheduled_time=scheduled.replace(minute=0, second=0, microsecond=0),
            status=status,
        )
        all_doses.append(dose)

    session.add_all(all_doses)
    session.flush()
    return all_doses


def seed():
    session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        # Users
        patient_user = get_or_create_user(session, "patient@example.com", UserRole.PATIENT, "Asha Pillai")
        patient2_user = get_or_create_user(session, "patient2@example.com", UserRole.PATIENT, "John Carter")
        patient3_user = get_or_create_user(session, "patient3@example.com", UserRole.PATIENT, "Emily Brown")
        caregiver_user = get_or_create_user(session, "caregiver@example.com", UserRole.CAREGIVER, "Lily Tran")
        doctor_user = get_or_create_user(session, "doctor@example.com", UserRole.DOCTOR, "Dr. Alex Lee")
        admin_user = get_or_create_user(session, "admin@example.com", UserRole.ADMIN, "Admin MedMind")

        # Profiles
        patient = session.query(Patient).filter(Patient.user_id == patient_user.id).first()
        if not patient:
            patient = Patient(
                id=_uuid(),
                user_id=patient_user.id,
                full_name=patient_user.full_name,
                dob=datetime(1962, 4, 12).date(),
                gender="female",
                notes="Hypertension, post-menopause, occasional dizziness",
            )
            session.add(patient)
        else:
            patient.dob = patient.dob or datetime(1962, 4, 12).date()
            patient.gender = patient.gender or "female"

        caregiver = session.query(Caregiver).filter(Caregiver.user_id == caregiver_user.id).first()
        if not caregiver:
            caregiver = Caregiver(id=_uuid(), user_id=caregiver_user.id, full_name=caregiver_user.full_name)
            session.add(caregiver)

        doctor = session.query(Doctor).filter(Doctor.user_id == doctor_user.id).first()
        if not doctor:
            doctor = Doctor(id=_uuid(), user_id=doctor_user.id, full_name=doctor_user.full_name, specialization="Cardiology")
            session.add(doctor)

        session.flush()

        session.add_all(
            [
                PatientCaregiver(id=_uuid(), patient_id=patient.id, caregiver_id=caregiver.id, is_primary=True),
                PatientDoctor(id=_uuid(), patient_id=patient.id, doctor_id=doctor.id, is_primary=True),
            ]
        )

        profile = session.query(PatientProfile).filter(PatientProfile.patient_id == patient.id).first()
        if not profile:
            profile = PatientProfile(
                id=_uuid(),
                patient_id=patient.id,
                avatar_url="https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=400&q=80",
                medical_history="Hypertension; post-menopause; mild osteoarthritis",
                allergies="None reported",
                primary_complaint="Occasional dizziness mid-morning",
                current_medications=["Amlodipine 5mg", "Atorvastatin 20mg"],
                lifestyle_factors=["Desk work", "Walks 5x/week", "Low-sodium diet"],
                recent_tests=["ECG - Normal sinus rhythm", "Lipid panel - Controlled"],
                treatment_plan=["Continue BP control", "Increase hydration", "Weekly BP log review"],
            )
            session.add(profile)

        # Device
        device = session.query(Device).filter(Device.device_uid == "MM-BOX-001").first()
        if not device:
            device = Device(
                id=_uuid(),
                device_uid="MM-BOX-001",
                device_key_hash="devkeyhash",
                firmware_version="1.0.0",
                status="PAIRED",
                paired_patient_id=patient.id,
                last_ip="192.168.1.50",
            )
            session.add(device)
            session.flush()
        else:
            device.paired_patient_id = patient.id
            session.flush()

        session.add(
            DeviceHeartbeat(
                id=_uuid(),
                device_id=device.id,
                battery="85%",
                temperature="34C",
                firmware_version=device.firmware_version,
                ip_address=device.last_ip,
                payload={"signal": "good"},
            )
        )

        # Medication catalog + plans
        med_bp = Medication(id=_uuid(), name="Amlodipine", generic_name="Amlodipine", form="tablet", strength="5", unit="mg")
        med_dm = Medication(id=_uuid(), name="Metformin", generic_name="Metformin", form="tablet", strength="500", unit="mg")
        med_chol = Medication(id=_uuid(), name="Atorvastatin", generic_name="Atorvastatin", form="tablet", strength="20", unit="mg")
        session.add_all([med_bp, med_dm, med_chol])
        session.flush()

        plan = MedicationPlan(
            id=_uuid(),
            patient_id=patient.id,
            doctor_id=doctor.id,
            caregiver_id=caregiver.id,
            name="Week 1 Plan",
            is_active=True,
        )
        session.add(plan)
        session.flush()

        item_bp = MedicationPlanItem(
            id=_uuid(),
            medication_plan_id=plan.id,
            medication_id=med_bp.id,
            dose_amount="1",
            dose_unit="tablet",
            frequency_pattern="BID",
            slot_id="A1",
            time_of_day="08:00;20:00",
            instructions="Take after breakfast",
        )
        item_dm = MedicationPlanItem(
            id=_uuid(),
            medication_plan_id=plan.id,
            medication_id=med_dm.id,
            dose_amount="1",
            dose_unit="tablet",
            frequency_pattern="BID",
            slot_id="B1",
            time_of_day="08:00;20:00",
            instructions="Take with dinner",
        )
        session.add_all([item_bp, item_dm])
        session.flush()

        doses = add_dense_doses(session, plan, [item_bp, item_dm], patient, device, now)
        _set_statuses(doses, taken_ratio=0.9, on_time_ratio=0.72)

        # Extra patients demo
        patient2 = session.query(Patient).filter(Patient.user_id == patient2_user.id).first()
        if not patient2:
            patient2 = Patient(
                id=_uuid(),
                user_id=patient2_user.id,
                full_name=patient2_user.full_name,
                dob=datetime(1958, 9, 17).date(),
                gender="male",
                notes="Hypertension; former smoker; borderline cholesterol",
            )
            session.add(patient2)
        else:
            patient2.dob = patient2.dob or datetime(1958, 9, 17).date()
            patient2.gender = patient2.gender or "male"

        patient3 = session.query(Patient).filter(Patient.user_id == patient3_user.id).first()
        if not patient3:
            patient3 = Patient(
                id=_uuid(),
                user_id=patient3_user.id,
                full_name=patient3_user.full_name,
                dob=datetime(1954, 2, 3).date(),
                gender="female",
                notes="Type 2 Diabetes; hypertension; angina history",
            )
            session.add(patient3)
        else:
            patient3.dob = patient3.dob or datetime(1954, 2, 3).date()
            patient3.gender = patient3.gender or "female"

        session.flush()

        session.add_all(
            [
                PatientDoctor(id=_uuid(), patient_id=patient2.id, doctor_id=doctor.id, is_primary=True),
                PatientDoctor(id=_uuid(), patient_id=patient3.id, doctor_id=doctor.id, is_primary=True),
            ]
        )

        profile2 = session.query(PatientProfile).filter(PatientProfile.patient_id == patient2.id).first()
        if not profile2:
            profile2 = PatientProfile(
                id=_uuid(),
                patient_id=patient2.id,
                avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
                medical_history="Hypertension",
                allergies="None reported",
                primary_complaint="Occasional chest pressure on exertion",
                current_medications=["Amlodipine 5mg", "Atorvastatin 10mg"],
                lifestyle_factors=["Former smoker", "Light cycling on weekends"],
                recent_tests=["Stress test - borderline", "BP log - mostly controlled"],
                treatment_plan=["Continue BP meds", "Add evening walk", "Reduce caffeine after 3pm"],
            )
            session.add(profile2)

        profile3 = session.query(PatientProfile).filter(PatientProfile.patient_id == patient3.id).first()
        if not profile3:
            profile3 = PatientProfile(
                id=_uuid(),
                patient_id=patient3.id,
                avatar_url="https://images.unsplash.com/photo-1500336624523-d727130c3328?auto=format&fit=crop&w=400&q=80&sat=-10",
                medical_history="Hypertension; Type 2 Diabetes; Angina history",
                allergies="Sulfa drugs",
                primary_complaint="Shortness of breath with stairs",
                current_medications=["Metformin 500mg", "Losartan 50mg", "Nitroglycerin PRN"],
                lifestyle_factors=["Retired teacher", "Morning walks", "Mediterranean diet"],
                recent_tests=["HbA1c - 7.2%", "Lipid profile - borderline", "Resting ECG - Normal"],
                treatment_plan=["Monitor angina symptoms", "Adherence coaching", "Cardio follow-up in 2 weeks"],
            )
            session.add(profile3)

        plan2 = MedicationPlan(
            id=_uuid(),
            patient_id=patient2.id,
            doctor_id=doctor.id,
            caregiver_id=caregiver.id,
            name="Blood Pressure Control",
            is_active=True,
        )
        session.add(plan2)
        session.flush()

        item2 = MedicationPlanItem(
            id=_uuid(),
            medication_plan_id=plan2.id,
            medication_id=med_bp.id,
            dose_amount="1",
            dose_unit="tablet",
            frequency_pattern="QD",
            slot_id="C1",
            time_of_day="08:00",
            instructions="Morning dose",
        )
        session.add(item2)
        session.flush()

        doses_p2 = add_dense_doses(session, plan2, [item2], patient2, None, now)
        _set_statuses(doses_p2, taken_ratio=0.9, on_time_ratio=0.7)

        plan3 = MedicationPlan(
            id=_uuid(),
            patient_id=patient3.id,
            doctor_id=doctor.id,
            caregiver_id=caregiver.id,
            name="Diabetes Control",
            is_active=True,
        )
        session.add(plan3)
        session.flush()

        item3 = MedicationPlanItem(
            id=_uuid(),
            medication_plan_id=plan3.id,
            medication_id=med_dm.id,
            dose_amount="1",
            dose_unit="tablet",
            frequency_pattern="BID",
            slot_id="D1",
            time_of_day="08:00;20:00",
            instructions="With meals",
        )
        session.add(item3)
        session.flush()

        doses_p3 = add_dense_doses(session, plan3, [item3], patient3, None, now)
        _set_statuses(doses_p3, taken_ratio=0.6894, on_time_ratio=0.62)

        # Dose event logs
        session.add_all(
            [
                DoseEventLog(
                    id=_uuid(),
                    dose_id=doses[0].id,
                    device_id=device.id,
                    event_type="DOSE_CONFIRMED",
                    payload={"slot": item_bp.slot_id},
                    event_time=doses[0].actual_time,
                ),
                DoseEventLog(
                    id=_uuid(),
                    dose_id=doses[1].id,
                    device_id=device.id,
                    event_type="MISSED_DOSE",
                    payload={"reason": "timeout"},
                    event_time=doses[1].scheduled_time + timedelta(minutes=45),
                ),
            ]
        )

        # Device events raw
        session.add_all(
            [
                DeviceEvent(
                    id=_uuid(),
                    device_id=device.id,
                    event_type="BOX_OPENED",
                    payload={"slot": item_bp.slot_id},
                    related_dose_id=doses[0].id,
                    event_time=doses[0].actual_time,
                ),
                DeviceEvent(
                    id=_uuid(),
                    device_id=device.id,
                    event_type="HEARTBEAT",
                    payload={"battery": "85%"},
                    event_time=now,
                ),
            ]
        )

        # Conversation & AI logs
        convo_id = _uuid()
        convo = Conversation(
            id=convo_id,
            patient_id=patient.id,
            device_id=device.id,
            started_at=now,
        )
        session.add(convo)
        session.flush()

        inter = InteractionLog(
            id=_uuid(),
            conversation_id=convo_id,
            patient_id=patient.id,
            device_id=device.id,
            speaker="PATIENT",
            source="VOICE",
            text_raw="Feeling light headache and dizziness today",
            text_normalized="feeling light headache and dizziness today",
            sentiment="neutral",
            meta={"wake_word": True},
        )
        session.add(inter)
        session.flush()

        llm_req = LLMRequest(
            id=_uuid(),
            conversation_id=convo_id,
            interaction_id=inter.id,
            patient_id=patient.id,
            device_id=device.id,
            intent="LOG_SYMPTOM",
            input_text=inter.text_normalized,
            output_text="Logged mild headache and dizziness.",
            model_name="demo-llm",
            latency_ms="1200",
            meta={"pipeline": "demo"},
        )
        session.add(llm_req)
        session.flush()

        # Distribute symptoms over the last 7 days for smoother bars and consistent trending counts.
        day = lambda d, h=0: now - timedelta(days=d, hours=h)
        symptom_logs_asha = [
            # Wed (0) total 3
            {"raw": "Chest pain with tightness while cooking", "severity": "severe", "created_at": day(0, 7), "symptoms": ["chest pain"]},
            {"raw": "Shortness of breath mild after stairs", "severity": "mild", "created_at": day(0, 6), "symptoms": ["shortness of breath"]},
            {"raw": "Headache dizziness mild evening", "severity": "mild", "created_at": day(0, 5), "symptoms": ["headache dizziness"]},
            # Tue (1) total 5
            {"raw": "Chest pain light pressure in evening", "severity": "moderate", "created_at": day(1, 18), "symptoms": ["chest pain"]},
            {"raw": "Chest pain when walking fast", "severity": "moderate", "created_at": day(1, 10), "symptoms": ["chest pain"]},
            {"raw": "Shortness of breath climbing stairs", "severity": "severe", "created_at": day(1, 9), "symptoms": ["shortness of breath"]},
            {"raw": "Headache dizziness after a short walk", "severity": "moderate", "created_at": day(1, 8), "symptoms": ["headache dizziness"]},
            {"raw": "Palpitations at night for a few minutes", "severity": "moderate", "created_at": day(1, 7), "symptoms": ["palpitations"]},
            # Mon (2) total 5
            {"raw": "Shortness of breath when walking uphill", "severity": "moderate", "created_at": day(2, 15), "symptoms": ["shortness of breath"]},
            {"raw": "Shortness of breath eased after rest", "severity": "moderate", "created_at": day(2, 11), "symptoms": ["shortness of breath"]},
            {"raw": "Headache dizziness mild, improved after rest", "severity": "mild", "created_at": day(2, 9), "symptoms": ["headache dizziness"]},
            {"raw": "Chest pain mild twinge in afternoon", "severity": "mild", "created_at": day(2, 14), "symptoms": ["chest pain"]},
            {"raw": "Nausea after breakfast", "severity": "mild", "created_at": day(2, 8), "symptoms": ["nausea"]},
            # Sun (3) total 3
            {"raw": "Headache dizziness worse at night", "severity": "moderate", "created_at": day(3, 21), "symptoms": ["headache dizziness"]},
            {"raw": "Lightheadedness on standing quickly", "severity": "mild", "created_at": day(3, 8), "symptoms": ["lightheadedness"]},
            {"raw": "Fatigue mid-afternoon, needed to sit", "severity": "mild", "created_at": day(3, 6), "symptoms": ["fatigue"]},
            # Sat (4) total 2
            {"raw": "Headache dizziness returned after lunch", "severity": "mild", "created_at": day(4, 14), "symptoms": ["headache dizziness"]},
            {"raw": "Chest pain fleeting, resolved after sitting", "severity": "mild", "created_at": day(4, 10), "symptoms": ["chest pain"]},
            # Additional new symptom spread
            {"raw": "Blurred vision brief episode", "severity": "mild", "created_at": day(2, 2), "symptoms": ["blurred vision"]},
        ]
        for sym in symptom_logs_asha:
            session.add(
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient.id,
                    severity=sym["severity"],
                    symptoms_raw=sym["raw"],
                    structured_json={"symptoms": sym["symptoms"], "severity": sym["severity"]},
                    created_at=sym["created_at"],
                )
            )

        session.add_all(
            [
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient2.id,
                    severity="mild",
                    symptoms_raw="Mild headache after evening walk",
                    structured_json={"symptoms": ["headache"], "severity": "mild"},
                    created_at=now - timedelta(days=3),
                ),
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient2.id,
                    severity="mild",
                    symptoms_raw="Brief lightheadedness after standing",
                    structured_json={"symptoms": ["lightheadedness"], "severity": "mild"},
                    created_at=now - timedelta(days=1, hours=3),
                ),
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient3.id,
                    severity="moderate",
                    symptoms_raw="Shortness of breath while gardening",
                    structured_json={"symptoms": ["shortness of breath"], "severity": "moderate"},
                    created_at=now - timedelta(days=2),
                ),
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient3.id,
                    severity="mild",
                    symptoms_raw="Mild chest discomfort after dinner",
                    structured_json={"symptoms": ["chest discomfort"], "severity": "mild"},
                    created_at=now - timedelta(days=1, hours=5),
                ),
            ]
        )
        alert = AlertLog(
            id=_uuid(),
            patient_id=patient.id,
            interaction_id=inter.id,
            llm_request_id=llm_req.id,
            symptoms="shortness of breath, chest pain",
            severity="high",
            onset_text="10 minutes ago",
            risk_score="0.8",
            risk_level="HIGH",
            structured_json={"emergency": True},
        )
        session.add(alert)

        # Notification demo
        channel = NotificationChannel(
            id=_uuid(),
            user_id=caregiver_user.id,
            channel="PUSH",
            address="fcm-token-demo",
            is_active=True,
        )
        session.add(channel)
        session.flush()

        notif_event = NotificationEvent(
            id=_uuid(),
            patient_id=patient.id,
            trigger_source="EMERGENCY_SIGNAL",
            related_alert_id=alert.id,
            title="Patient reported chest pain",
            body="Check on patient immediately.",
            data_payload={"risk": "HIGH"},
        )
        session.add(notif_event)
        session.flush()

        session.add(
            NotificationDelivery(
                id=_uuid(),
                notification_event_id=notif_event.id,
                channel_id=channel.id,
                status="SENT",
                send_attempts=1,
                sent_at=now,
            )
        )

        session.commit()
        print("✅ Seed data inserted (dense English demo).")
    except Exception as exc:  # pragma: no cover - dev helper
        session.rollback()
        print(f"Seed failed: {exc}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
