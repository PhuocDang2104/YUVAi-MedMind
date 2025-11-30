# 🌐 MedMind / YUVAi - Smart Medication Adherence Stack

<p align="center">
  <b>Edge AI pill box + FastAPI backend + Next.js portals for caregivers, doctors, and admins.</b><br>
  <i>Designed to impress judges: clear story, production-ready stack, and demo-friendly flows.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Edge-AI%20ASR%20%2B%20CV-blue" alt="Edge AI badge">
  <img src="https://img.shields.io/badge/Backend-FastAPI%20%7C%20Postgres%20%2B%20pgvector-green" alt="Backend badge">
  <img src="https://img.shields.io/badge/Frontend-Next.js%20(App%20Router)-black" alt="Frontend badge">
  <img src="https://img.shields.io/badge/AI-RAG%20%7C%20Tool--calling%20%7C%20LLM--Analytics-orange" alt="AI badge">
</p>

---

## 📖 Overview
- Problem: Older adults living alone miss or mis-dose medication; families and clinicians react late, causing avoidable hospitalizations and stress.
- Personas: Elderly patients (voice + pill box), caregivers (live adherence view), doctors (trusted longitudinal data to adjust treatment).
- Solution: Smart pill box with wake-word ASR and CV, a cloud intent router + RAG/LLM with tool-calling, and persona-first portals.
- Outcome: Better adherence, earlier warning signals, and clinical-grade visibility for families and providers.

## ✨ Highlights (judge-ready)
- Edge-first: Wake-word, on-device ASR/TTS (Vosk/Whisper tiny), CV for dose-taking confirmation.
- Cloud intelligence: Classifier gateway (intent + emergency), LLM-Core with RAG and tool-calling, LLM-Analytics for weekly insights and risk scores.
- Persona portals: Caregiver (mobile-first), Doctor (analytics), Admin/CS (ops) built on Next.js App Router.
- Resilient demos: Seed data, deterministic fallbacks when LLM fails, and API stubs that are ready to swap in real services.

## 🏗️ System Architecture (4 layers)
```
Device Edge - Smart Medicine Box
  - Wake-word + tiny ASR/TTS, lightweight CV for dose-taking
  - Servo-locked slots, LED/buzzer, buttons, camera + mic
  - Sends REMINDER_TRIGGERED / BOX_OPENED / DOSE_CONFIRMED / MISSED_DOSE / HEARTBEAT / voice

Communication - HTTPS / REST
  - GET /api/devices/{id}/schedule
  - POST /api/devices/{id}/events, /sync, /voice
  - Auth + dashboard APIs for apps/web

Backend and AI - FastAPI + Postgres/pgvector
  - Device + medication plans, dose events/logs, notifications
  - AI Gateway + RAG + tool-calling, analytics jobs (weekly summaries, insights, risk scores)

Clients - Next.js portals
  - Caregiver (mobile-first), Doctor (web analytics), Admin/CS (ops)
```

## 🧠 AI Brain (3 tiers)
- Edge AI: wake-word, on-device ASR (Vosk/Whisper tiny), CV (YOLO-Nano/MobileNet) to validate physical dose-taking.
- Classifier Gateway: intent + emergency detection (LOG_SYMPTOM, ASK_MEDICATION, DATA_QUERY, EMERGENCY_SIGNAL, SMALL_TALK) with safety rules and routing.
- LLM-Core + RAG + Tools: real-time chat, symptom extraction, medication Q&A, adherence summaries via tool calls (`get_adherence`, `get_symptom_log`, `get_medication_plan`, `get_weekly_summary`, `log_symptom`, `notify_caregiver`).
- LLM-Analytics: batch agent that mines weeks of logs into insights, risk scores, and weekly reports reused by LLM-Core.

## 🔌 Core APIs (high level)
- Devices: `GET /api/devices/{device_id}/schedule`, `POST /events`, `POST /sync`, `POST /voice`.
- Auth: `POST /api/auth/register`, `POST /api/auth/login`.
- Medication plans: `POST /api/medication_plans`, mappings slot_id <-> drugs.
- Dashboards and summaries: `GET /api/summary/weekly/{patient_id}`, `GET /api/dashboard/patient/{patient_id}`.
- AI chat: `POST /api/ai/chat` for layer1 summary / layer2 suggestion (LLM-backed, with fallback).

## 📊 Data Model Snapshot (Postgres)
- Users and persona links: `users`, `patients`, `caregivers`, `doctors`, joins `patient_caregiver`, `patient_doctor`.
- Device and telemetry: `devices`, `device_heartbeats`, `device_events`.
- Medication and adherence: `medications`, `medication_plans`, `medication_plan_items`, `dose_occurrences`, `dose_event_logs`.
- Conversation and AI: `conversations`, `interaction_logs`, `llm_requests`, `symptom_logs`, `medication_question_logs`, `alert_logs`.
- Notifications and delivery: `notification_channels`, `notification_events`, `notification_deliveries`.
- Analytics: `daily_patient_summaries`, `weekly_patient_summaries`, `health_insights`, `health_reports`, `embeddings`.

## 🚀 Demo Flows (tell the story)
- Use-case 1: Remind and confirm on the box - schedule sync, LED/voice reminder, BOX_OPENED/DOSE_CONFIRMED/MISSED_DOSE logged; notify on repeated misses.
- Use-case 2: Voice to structured symptom log - patient says "hoi dau dau", ASR -> intent LOG_SYMPTOM -> symptom_logs + friendly reply -> Health Log visible to family.
- Use-case 3: Emergency detection - "kho tho, dau nguc" flags EMERGENCY_SIGNAL, triggers alert + calming reply + caregiver push/SMS hooks.
- Use-case 4: Longitudinal insights - batch job mines dose_event_logs + symptom_logs -> health_insights, weekly_summaries -> doctor dashboard + PDF/export hooks.

## 🛠️ Tech Stack
- Backend: FastAPI, SQLAlchemy, Postgres + pgvector, Alembic-ready, Redis stream (optional), UVicorn.
- AI: Provider-agnostic chat clients (OpenAI/vLLM/TGI/Ollama), RAG over pgvector, tool-calling bridge, resilience via fallbacks.
- Frontend: Next.js (App Router), Chart.js, persona-scoped CSS.
- Edge assumptions: Raspberry Pi 4/5, servo-locked compartments, RGB LED + buzzer, buttons, camera, I2S/analog mic.

## 🖥️ Getting Started (dev)
```bash
# 1) Postgres
docker compose up -d db

# 2) Backend
cd backend
python -m venv .venv && .\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
$env:PYTHONPATH="."
python -m app.db.init_db              # quick schema for dev
uvicorn app.main:app --reload --port 8000

# 3) Frontend
cd ../frontend
npm install
cp .env.example .env.local
npm run dev                           # NEXT_PUBLIC_API_URL -> backend

# 4) Seed mock data (optional)
cd ../backend
$env:PYTHONPATH="."
python -m app.db.seed
```

## 📂 Repository Structure
```bash
YUVAi/
|-- backend/                   # FastAPI app, AI workspace, DB models, seeds
|   |-- app/
|   |   |-- api/v1/endpoints/  # auth, devices, events, medication_plans, summary, doctor, ai_chat, voice
|   |   |-- ai/                # prompts, gateway, provider registry, data samples
|   |   |-- db/                # session, init_db, seed, Alembic-ready base
|   |   |-- models/            # SQLAlchemy models (users, devices, meds, logs, analytics)
|   |   `-- schemas/           # Pydantic schemas
|   |-- alembic/               # migrations scaffold
|   |-- requirements.txt
|   `-- README.md
|-- frontend/                  # Next.js App Router portals (caregiver, doctor, admin)
|   |-- app/                   # routes per persona + layout
|   |-- components/            # nav, charts, chat widget
|   |-- styles/                # globals + persona-specific CSS
|   `-- README.md
|-- docker-compose.yml         # Postgres dev service
|-- temp_seed_edit.py          # helper for demo seed tweaks
`-- README.md                  # this file
```
- Extend easily: add device firmware docs and BOM under `docs/`; grow analytics jobs under `backend/app/ai` and migrations in `backend/alembic`; plug real charts by swapping mock APIs in `frontend/lib/api.ts`.

## 🤝 Team
- Đặng Như Phước
- Huỳnh Trọng Khiêm

## ✅ Next Steps (suggested)
1) Harden auth and RBAC; wire portals to issued tokens.
2) Turn RAG + tool-calling into a LangGraph flow per intent.
3) Add worker (Celery/Redis Stream) for voice/LLM + notifications; shift analytics to cron/batch.
4) Publish device firmware guide with wiring and bill of materials.
5) Add Playwright/Cypress + Pytest suites on seeded data for demo reliability.
