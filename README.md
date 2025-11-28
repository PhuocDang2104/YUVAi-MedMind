# YUVAi / MedMind Scaffold

Starter scaffold for a smart medicine box stack: Edge Device ↔ REST ↔ FastAPI ↔ Next.js portal. Default setup is dev-friendly but structured for production hardening.

## Repository Layout
- `backend/` – FastAPI, Postgres/pgvector, optional Redis stream.
- `frontend/` – Next.js (App Router) for Caregiver, Doctor, Admin portals.
  - `app/` – routes per persona.
  - `components/`, `lib/`, `styles/`.
  - CSS split per navigation: `styles/globals.css` (shared layout), `styles/caregiver.css`, `styles/doctor.css`, `styles/admin.css`.
- `docker-compose.yml` – Postgres dev service.
- `README.md` (root), `backend/README.md`, `frontend/README.md` for persona-specific instructions.

## Quickstart (dev)
```bash
# 1) Postgres
docker compose up -d db

# 2) Backend
cd backend
python -m venv .venv && .\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
$env:PYTHONPATH="."
python -m app.db.init_db
uvicorn app.main:app --reload --port 8000

# 3) Frontend
cd ../frontend
npm install
cp .env.example .env.local
npm run dev

# 4) Seed demo data (optional, for mock API)
cd ../backend
$env:PYTHONPATH="."
python -m app.db.seed
```

## Personas & Navigation
- Caregiver (mobile-style): `/caregiver/*` – Home, Health Log, Medication, Alerts, Profile.
- Doctor (web): `/doctor/*` – Dashboards (overall/patient/alerts), Patients, Medication Plans, Symptom Analytics, AI Insights, Reports.
- Admin/CS (web): `/admin/*` – Dashboard, Devices, Device Events, Users, Patients, Logs, System Health, Settings.
- Login/persona switch at `/`.

## Data & AI Flow (high level)
- Edge box ↔ Backend: schedule fetch + event/voice posts.
- Frontend ↔ Backend: REST via `NEXT_PUBLIC_API_URL`.
- AI pipeline stub in `backend/app/services/LLMPipeline`; batch jobs intended for analytics (`health_insights`, summaries).

## Next Steps
- Add Alembic migrations instead of `create_all`.
- Implement auth + RBAC for personas.
- Wire real charts/data to API, keep per-nav CSS for easy theming.
- Add queue/worker for voice/LLM + notification delivery and expand tests (Pytest, Playwright/Cypress).
