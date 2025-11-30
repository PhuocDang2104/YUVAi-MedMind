"use client";

import { useState } from "react";

type DailyReport = {
  dateLabel: string;
  adherence: string;
  criticalEvents: number;
  symptomsLogged: number;
  adherenceNote: string;
  symptomNote: string;
  riskNote: string;
  actions: string[];
};

type WeeklyReport = {
  weekLabel: string;
  avgAdherence: string;
  criticalEvents: number;
  mostMissedSlot: string;
  adherencePattern: string;
  symptomTrend: string;
  riskSignals: { time: string; label: string; severity: string }[];
  plan: string[];
};

type WarningCard = {
  category: string;
  title: string;
  timeScope: string;
  summary: string;
  impact: string;
  confidence: string;
  actions: string[];
  severity: string;
};

const patients = [
  { id: "asha", name: "Asha Pillai", meta: "63 y/o · Hypertension, dizziness" },
  { id: "emily", name: "Emily Brown", meta: "59 y/o · CAD, statin therapy" },
  { id: "john", name: "John Carter", meta: "66 y/o · CHF, beta blocker" }
];

const dailyData: Record<string, DailyReport[]> = {
  asha: [
    {
      dateLabel: "Today (Sat, 29 Nov 2025)",
      adherence: "82%",
      criticalEvents: 1,
      symptomsLogged: 3,
      adherenceNote: "Evening Amlodipine was skipped once; morning doses on time.",
      symptomNote: "Dizziness appeared after skipping evening Metformin.",
      riskNote: "Shortness of breath + chest pain occurred once; HIGH risk signal detected.",
      actions: [
        "Call before 20:00 to reinforce evening meds.",
        "Remind Metformin before bedtime.",
        "Ask patient to call doctor if chest pain repeats."
      ]
    },
    {
      dateLabel: "Yesterday (Fri, 28 Nov 2025)",
      adherence: "86%",
      criticalEvents: 0,
      symptomsLogged: 2,
      adherenceNote: "Late evening dose but taken within 45 minutes.",
      symptomNote: "Mild headache after late dose; resolved without meds.",
      riskNote: "No high-risk events detected yesterday.",
      actions: [
        "Send gentle reminder 30 minutes before evening slot.",
        "Encourage hydration with evening meds."
      ]
    }
  ],
  emily: [
    {
      dateLabel: "Today (Sat, 29 Nov 2025)",
      adherence: "78%",
      criticalEvents: 1,
      symptomsLogged: 2,
      adherenceNote: "Evening statin missed; morning doses on time.",
      symptomNote: "Reported chest tightness after stairs.",
      riskNote: "Chest tightness once; MODERATE risk signal.",
      actions: [
        "Call caregiver to reinforce evening statin.",
        "Limit exertion today; monitor chest symptoms.",
        "Escalate if tightness recurs."
      ]
    }
  ],
  john: [
    {
      dateLabel: "Today (Sat, 29 Nov 2025)",
      adherence: "88%",
      criticalEvents: 0,
      symptomsLogged: 1,
      adherenceNote: "All beta blocker doses on time.",
      symptomNote: "Mild fatigue mid-afternoon.",
      riskNote: "No high-risk events detected today.",
      actions: [
        "Maintain current schedule.",
        "Encourage light activity and hydration."
      ]
    }
  ]
};

const weeklyData: Record<string, WeeklyReport[]> = {
  asha: [
    {
      weekLabel: "Week of 24–30 Nov 2025",
      avgAdherence: "80%",
      criticalEvents: 2,
      mostMissedSlot: "Evening Amlodipine",
      adherencePattern: "Evening doses are missed more often on weekends, especially the Amlodipine slot.",
      symptomTrend: "Dizziness after skipping evening Metformin occurred in 3/5 recorded episodes.",
      riskSignals: [
        { time: "Thu 21:35", label: "Shortness of breath + chest pain", severity: "HIGH" },
        { time: "Tue 09:10", label: "Dizziness on standing", severity: "MODERATE" }
      ],
      plan: [
        "Move evening dose to morning temporarily.",
        "Ask patient to record blood pressure every morning.",
        "Schedule a follow-up call mid-week."
      ]
    }
  ],
  emily: [
    {
      weekLabel: "Week of 24–30 Nov 2025",
      avgAdherence: "76%",
      criticalEvents: 1,
      mostMissedSlot: "Evening Statin",
      adherencePattern: "Statin missed twice; morning doses more reliable.",
      symptomTrend: "Chest tightness after exertion reported twice.",
      riskSignals: [{ time: "Wed 19:20", label: "Chest tightness after stairs", severity: "MODERATE" }],
      plan: [
        "Add pre-evening reminder push.",
        "Encourage slower stair use and rest breaks.",
        "Check lipid panel date and book follow-up."
      ]
    }
  ],
  john: [
    {
      weekLabel: "Week of 24–30 Nov 2025",
      avgAdherence: "84%",
      criticalEvents: 0,
      mostMissedSlot: "None",
      adherencePattern: "Consistent beta blocker timing; occasional late evening doses.",
      symptomTrend: "Fatigue noted twice after lunch.",
      riskSignals: [],
      plan: [
        "Keep same schedule.",
        "Encourage hydration and light walks."
      ]
    }
  ]
};

const warningData: Record<string, WarningCard[]> = {
  asha: [
    {
      category: "Risk Signal",
      title: "Shortness of breath + chest pain",
      timeScope: "Past 24h",
      summary: "Shortness of breath + chest pain occurred once; risk level HIGH.",
      impact: "Potential cardiac event risk; needs close monitoring.",
      confidence: "High",
      severity: "HIGH",
      actions: [
        "Prioritize push to caregiver.",
        "Ask patient to call doctor if it repeats.",
        "Flag alert as critical."
      ]
    },
    {
      category: "Adherence",
      title: "Evening Amlodipine missed",
      timeScope: "Past 48h",
      summary: "Evening Amlodipine missed once; pattern noted on weekends.",
      impact: "Potential BP rebound overnight.",
      confidence: "Medium",
      severity: "MODERATE",
      actions: [
        "Send pre-evening reminder.",
        "Call before 20:00."
      ]
    }
  ],
  emily: [
    {
      category: "Risk Signal",
      title: "Chest tightness after stairs",
      timeScope: "Past 72h",
      summary: "Chest tightness after exertion; risk level MODERATE.",
      impact: "Possible exertional angina; monitor closely.",
      confidence: "Medium",
      severity: "MODERATE",
      actions: [
        "Advise rest and slower stair use.",
        "Follow up if repeats."
      ]
    }
  ],
  john: [
    {
      category: "Adherence",
      title: "Late evening dose",
      timeScope: "Past 24h",
      summary: "Evening dose taken late but within window.",
      impact: "Minimal impact; continue monitoring.",
      confidence: "High",
      severity: "LOW",
      actions: [
        "Keep reminder cadence.",
        "No escalation needed."
      ]
    }
  ]
};

type Mode = "daily" | "weekly" | "warnings";

export default function AIInsights() {
  const [patientId, setPatientId] = useState<string>("asha");
  const [mode, setMode] = useState<Mode>("daily");

  const patient = patients.find((p) => p.id === patientId) || patients[0];
  const daily = dailyData[patient.id] || [];
  const weekly = weeklyData[patient.id] || [];
  const warnings = warningData[patient.id] || [];

  return (
    <main className="doctor-page" style={{ gap: 16 }}>
      <header className="card insights-hero">
        <div className="hero-left">
          <div className="pill soft">AI Insights</div>
          <h2>Clinical-grade medication and symptom insights per patient</h2>
          <p className="muted">Daily and weekly summaries plus critical warnings synthesized by MedMind.</p>
        </div>
        <div className="hero-controls">
          <div className="combo">
            <label className="muted">Select patient</label>
            <select value={patientId} onChange={(e) => setPatientId(e.target.value)}>
              {patients.map((p) => (
                <option key={p.id} value={p.id}>{p.name} · {p.meta}</option>
              ))}
            </select>
          </div>
          <div className="mode-toggle">
            {[
              { id: "daily", label: "Daily" },
              { id: "weekly", label: "Weekly" },
              { id: "warnings", label: "Warnings" }
            ].map((m) => (
              <button
                key={m.id}
                className={`mode-btn ${mode === m.id ? "active" : ""}`}
                onClick={() => setMode(m.id as Mode)}
              >
                {m.label}
              </button>
            ))}
          </div>
        </div>
      </header>

      {mode === "daily" && (
        <section className="grid" style={{ gap: 12 }}>
          {daily.map((d) => (
            <article key={d.dateLabel} className="card large">
              <div className="card-head">
                <div>
                  <div className="pill soft">Daily AI Insight Summary</div>
                  <h3 style={{ margin: "6px 0 4px" }}>{d.dateLabel}</h3>
                </div>
                <div className="pill" style={{ background: "rgba(99,102,241,0.12)", color: "#4338ca" }}>
                  AI-generated ✦
                </div>
              </div>
              <div className="metric-strip">
                <span className="chip-lg info">Adherence: {d.adherence}</span>
                <span className="chip-lg danger">Critical events: {d.criticalEvents}</span>
                <span className="chip-lg warning">Symptoms logged: {d.symptomsLogged}</span>
              </div>
              <div className="section">
                <div className="label">Adherence & Routine</div>
                <p>{d.adherenceNote}</p>
              </div>
              <div className="section">
                <div className="label">Symptoms & Medication</div>
                <p>{d.symptomNote}</p>
              </div>
              <div className="section">
                <div className="label">Risk & Alerts</div>
                <p>{d.riskNote}</p>
              </div>
              <div className="section">
                <div className="label">Recommended Actions</div>
                <ul className="action-list">
                  {d.actions.map((a) => (
                    <li key={a}>{a}</li>
                  ))}
                </ul>
              </div>
            </article>
          ))}
        </section>
      )}

      {mode === "weekly" && (
        <section className="grid" style={{ gap: 12 }}>
          {weekly.map((w) => (
            <article key={w.weekLabel} className="card large">
              <div className="card-head">
                <div>
                  <div className="pill soft">Weekly AI Summary</div>
                  <h3 style={{ margin: "6px 0 4px" }}>{w.weekLabel}</h3>
                </div>
              </div>
              <div className="metric-strip">
                <span className="chip-lg info">Average adherence: {w.avgAdherence}</span>
                <span className="chip-lg danger">Critical events: {w.criticalEvents}</span>
                <span className="chip-lg">Most missed slot: {w.mostMissedSlot}</span>
              </div>
              <div className="section">
                <div className="label">Weekly Adherence Pattern</div>
                <p>{w.adherencePattern}</p>
              </div>
              <div className="section">
                <div className="label">Symptom–Medication Trends</div>
                <p>{w.symptomTrend}</p>
              </div>
              <div className="section">
                <div className="label">Risk Signals Recap</div>
                {w.riskSignals.length ? (
                  <ul className="action-list">
                    {w.riskSignals.map((r) => (
                      <li key={r.time}>
                        <strong>{r.time}</strong> — {r.label} ({r.severity})
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No high-risk signals this week.</p>
                )}
              </div>
              <div className="section">
                <div className="label">Plan for Next Week</div>
                <ul className="action-list">
                  {w.plan.map((p) => (
                    <li key={p}>{p}</li>
                  ))}
                </ul>
              </div>
            </article>
          ))}
        </section>
      )}

      {mode === "warnings" && (
        <section className="grid" style={{ gap: 12 }}>
          <div className="card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div className="pill soft danger">Critical summary</div>
              <div className="muted">Last 7 days · {warnings.length} critical insights</div>
            </div>
            <div className="muted">Last critical event: 2025-11-28 21:35</div>
          </div>
          {warnings.map((w) => (
            <article key={w.title} className="card warning-card">
              <div className="card-head">
                <div className="pill soft">{w.category}</div>
                <div className="pill soft" style={{ background: "rgba(239,68,68,0.12)", color: "#b91c1c" }}>
                  Severity: {w.severity}
                </div>
              </div>
              <div className="muted" style={{ fontSize: 12, marginBottom: 6 }}>{w.timeScope}</div>
              <h4 style={{ margin: "4px 0" }}>{w.title}</h4>
              <p style={{ margin: "6px 0" }}>{w.summary}</p>
              <div className="muted" style={{ marginBottom: 6 }}>Impact: {w.impact}</div>
              <div className="muted" style={{ marginBottom: 8 }}>Confidence: {w.confidence}</div>
              <div className="label">Suggested actions</div>
              <ul className="action-list">
                {w.actions.map((a) => (
                  <li key={a}>{a}</li>
                ))}
              </ul>
            </article>
          ))}
        </section>
      )}
    </main>
  );
}
