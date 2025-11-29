# Backend (FastAPI) – MedMind

## Overview
- Edge device: REST endpoints (`/devices/{id}/schedule`, `/events`, `/voice`) → FastAPI stores to DB and triggers pipelines.
- Frontend: uses `NEXT_PUBLIC_API_URL` to pull dashboard/schedule/summary data.
- AI server-side: `app/services/LLMPipeline` (stub) to process audio → intent/extraction → write `symptom_logs`/`alert_logs` and `notification_events`.
- Batch/Cloud: periodic jobs to generate `health_insights`, daily/weekly summaries; frontend reads these analytics tables.

## Code Layout
- `app/main.py` – FastAPI init, CORS, mounts v1 router.
- `app/api/v1/` – endpoints (auth, devices, events, voice, medication_plans, summary).
- `app/core/config.py` – settings (.env).
- `app/db/session.py` – SessionLocal; `app/db/init_db.py` – quick dev schema via `create_all`.
- `app/models/`, `app/schemas/` – SQLAlchemy models + Pydantic schemas.
- `app/ai/` – AI workspace (gateway, prompts, provider registry for OpenAI/vLLM/Ollama, docs in `app/ai/README.md`).
- `app/services/` – orchestration/AI stubs wired to the AI workspace.
- `tests/` – Pytest home.

## Schema (Postgres)
- Users & Profiles: `users`, `patients`, `caregivers`, `doctors`, joins `patient_caregiver`, `patient_doctor`.
- Device: `devices`, `device_heartbeats`, `device_events`.
- Medication: `medications`, `medication_plans`, `medication_plan_items`, `dose_occurrences`, `dose_event_logs`.
- Conversation & AI: `conversations`, `interaction_logs`, `llm_requests`, `symptom_logs`, `medication_question_logs`, `alert_logs`.
- Notifications: `notification_channels`, `notification_events`, `notification_deliveries`.
- Analytics & Reports: `daily_patient_summaries`, `weekly_patient_summaries`, `health_insights`, `health_reports`, `embeddings`.

## Run & Init DB (dev)
```bash
# from repo root
docker compose up -d db

cd backend
python -m venv .venv && .\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
$env:PYTHONPATH="."
python -m app.db.init_db   # quick dev schema via create_all

uvicorn app.main:app --reload --port 8000
```
> For production use Alembic migrations instead of `create_all`.

### Alembic
```bash
cd backend
$env:PYTHONPATH="."
alembic revision --autogenerate -m "init schema"
alembic upgrade head
```

### Seed Mock Data
```bash
cd backend
$env:PYTHONPATH="."
python -m app.db.seed
```
Creates demo users/patients/devices, medication plan, dose occurrences (ON_TIME/LATE/MISSED), device events, symptom/medication question/alert logs, notification sample.

## Next Steps
1) Replace stub services with real schedule generation + notification delivery.
2) Add JWT auth + RBAC.
3) Introduce queue/worker (Redis/Celery/Stream) for voice/LLM + notification pipelines.
4) Enable pgvector where embeddings are stored.
5) Expand tests and observability.
