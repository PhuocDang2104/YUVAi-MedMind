# Frontend – MedMind Portal

Next.js App Router UI for three personas: Caregiver (mobile), Doctor, and Admin.

## Structure
- `app/`
  - `/` – login/persona selection.
  - `/caregiver/*` – Home, Health Log, Medication, Alerts, Profile.
  - `/doctor/*` – Dashboards (overall/patient/alerts), Patients, Medication Plans, Symptom Analytics, AI Insights, Reports.
  - `/admin/*` – Dashboard, Devices, Device Events, Users, Patients, Logs, System Health, Settings.
- `components/` – shared UI (Topbar, SidebarNav, CaregiverNav, charts).
- `styles/`
  - `globals.css` – base theme/layout (shell, topbar, sidebar, cards).
  - `caregiver.css`, `doctor.css`, `admin.css` – content styling per navigation.
- `lib/` – helpers (`api`, `types`).

## Run Dev
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```
`NEXT_PUBLIC_API_URL` should point to the FastAPI backend.

## Design Notes
- Light theme with shared shell (sticky topbar + sidebar).
- Charts via Chart.js with compact sizing and alert markers on patient timelines.
- Copy is fully English; dummy data can be swapped via `lib/api.ts`.

## Extending
- Replace mock chart placeholders with live data.
- Use per-nav CSS files to tweak layouts without touching global shell styles.
- Add real auth/guarded routes once backend auth is ready.
