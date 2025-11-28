"use client";

import { useEffect, useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { getDoctorPatients, getPatientDashboard } from "../../../../lib/api";
import type {
  DashboardHorizon,
  DoctorPatient,
  PatientDashboard as PatientDashboardType,
  SeverityTrend,
  SymptomTrending
} from "../../../../lib/types";

const StackedBar = dynamic(() => import("../../../../components/StackedBar"), { ssr: false });

type StatusBadge = { label: string; color: string };

const adherenceScale = (value?: number | null): StatusBadge => {
  if (value === undefined || value === null) return { label: "n/a", color: "var(--muted)" };
  if (value >= 90) return { label: "Optimal", color: "var(--success)" };
  if (value >= 70) return { label: "Watch", color: "var(--warning)" };
  return { label: "Critical", color: "var(--danger)" };
};

const severityBadge = (trend?: SeverityTrend): StatusBadge => {
  if (!trend) return { label: "Flat", color: "var(--muted)" };
  if (trend.direction === "up") return { label: `Severity up ${Math.abs(trend.change_pct)}%`, color: "var(--warning)" };
  if (trend.direction === "down") return { label: `Severity down ${Math.abs(trend.change_pct)}%`, color: "var(--success)" };
  return { label: "Severity stable", color: "var(--muted)" };
};

const formatDate = (value?: string | null) =>
  value ? new Date(value).toLocaleString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }) : "-";

const initials = (name?: string) =>
  name
    ? name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .slice(0, 2)
        .toUpperCase()
    : "";

const renderList = (items?: string[], fallback?: string) =>
  items && items.length > 0 ? (
    <div className="tag-row">
      {items.map((item) => (
        <span key={item} className="soft-pill">
          {item}
        </span>
      ))}
    </div>
  ) : (
    <span className="muted">{fallback || "No data"}</span>
  );

export default function DoctorPatientDashboard() {
  const [patients, setPatients] = useState<DoctorPatient[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [dashboard, setDashboard] = useState<PatientDashboardType | null>(null);
  const [loading, setLoading] = useState(false);
  const [horizon, setHorizon] = useState<DashboardHorizon>("week");

  useEffect(() => {
    getDoctorPatients()
      .then((res) => {
        setPatients(res.patients || []);
        if (res.patients?.[0]?.id) {
          setSelected(res.patients[0].id);
        }
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!selected) return;
    setLoading(true);
    getPatientDashboard(selected, horizon)
      .then(setDashboard)
      .catch(() => setDashboard(null))
      .finally(() => setLoading(false));
  }, [selected, horizon]);

  const selectedPatient = useMemo(() => patients.find((p) => p.id === selected) || null, [patients, selected]);
  const adherenceStatus = adherenceScale(dashboard?.adherence.overall_adherence_rate);
  const severityStatus = severityBadge(dashboard?.symptoms.severity_trend);

  const trendingSymptoms: SymptomTrending[] = (dashboard?.symptoms.trending || []).slice(0, 3);
  const newSymptoms = (dashboard?.symptoms.new_symptoms || []).slice(0, 3);
  const severityBars = dashboard?.symptoms.severity_bars || [];
  const severityLabels = severityBars.map((b) => b.label);
  const severityData = [
    { label: "Normal", values: severityBars.map((b) => b.normal), color: "#22c55e" },
    { label: "Warning", values: severityBars.map((b) => b.warning), color: "#f59e0b" },
    { label: "Alert", values: severityBars.map((b) => b.alert), color: "#ef4444" }
  ];

  return (
    <main className="doctor-page" style={{ gap: 14 }}>
      <section className="card profile-card">
        <div className="profile-card__header">
          <div>
            <div className="pill">Patient Profile</div>
            <h2 style={{ margin: "6px 0 2px" }}>{dashboard?.patient.name || "Select a patient"}</h2>
            {selectedPatient && (
              <div className="muted" style={{ fontSize: 13 }}>
                Snapshot updates by patient and horizon
              </div>
            )}
          </div>
          <div className="profile-selector" style={{ display: "flex", gap: 10, alignItems: "flex-end", flexWrap: "wrap" }}>
            <div style={{ display: "grid", gap: 6 }}>
              <label className="muted" style={{ fontSize: 12 }}>
                Switch patient
              </label>
              <select value={selected || ""} onChange={(e) => setSelected(e.target.value)}>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
            </div>
            <div style={{ display: "grid", gap: 6 }}>
              <label className="muted" style={{ fontSize: 12 }}>
                Horizon
              </label>
              <div className="pill-row">
                {(["week", "month"] as DashboardHorizon[]).map((h) => (
                  <button
                    key={h}
                    onClick={() => setHorizon(h)}
                    className="ghost-pill"
                    style={{
                      background: horizon === h ? "rgba(37,99,235,0.12)" : "#fff",
                      borderColor: horizon === h ? "var(--primary)" : "var(--border)",
                      color: horizon === h ? "var(--text)" : "var(--muted)"
                    }}
                  >
                    {h === "week" ? "Past 7 days" : "Past 30 days"}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
        <div className="profile-card__body">
          <div className="profile-main">
            <div className="profile-identity">
              <div className="profile-avatar">
                {dashboard?.patient.avatar_url ? <img src={dashboard.patient.avatar_url} alt={dashboard.patient.name} /> : initials(dashboard?.patient.name)}
              </div>
              <div>
                <div className="profile-name-row">
                  <span className="profile-name">{dashboard?.patient.name || "-"}</span>
                  <span className="status-dot" style={{ background: adherenceStatus.color }} />
                  <span className="muted" style={{ fontSize: 13 }}>
                    {adherenceStatus.label}
                  </span>
                </div>
                <div className="muted" style={{ display: "flex", gap: 12, marginTop: 6, fontSize: 13 }}>
                  <span>Age: {dashboard?.patient.age ?? "-"}</span>
                  <span>Gender: {dashboard?.patient.gender || "-"}</span>
                </div>
              </div>
            </div>
            <div className="profile-data-grid">
              <div>
                <div className="label">Medical History</div>
                {renderList(dashboard?.patient.medical_history, "No history logged")}
              </div>
              <div>
                <div className="label">Current Medications</div>
                {renderList(dashboard?.patient.current_medications, "No active meds")}
              </div>
              <div>
                <div className="label">Allergies</div>
                {renderList(dashboard?.patient.allergies, "None reported")}
              </div>
              <div>
                <div className="label">Primary Complaint</div>
                <p style={{ margin: 0 }}>{dashboard?.patient.primary_complaint || "No complaint captured"}</p>
              </div>
            </div>
          </div>
          <div className="profile-sidebar">
            <div className="sidebar-block">
              <div className="label">Lifestyle Factors</div>
              {renderList(dashboard?.patient.lifestyle_factors, "No lifestyle notes")}
            </div>
            <div className="sidebar-block">
              <div className="label">Recent Tests</div>
              {renderList(dashboard?.patient.recent_tests, "No tests logged")}
            </div>
            <div className="sidebar-block">
              <div className="label">Treatment Plan</div>
              {renderList(dashboard?.patient.treatment_plan, "No plan available")}
            </div>
          </div>
        </div>
        {loading && <div className="muted" style={{ marginTop: 8 }}>Loading patient metrics...</div>}
      </section>

      <section className="card kpi-section compact">
        <div className="kpi-header">
          <div>
            <div className="pill">Medication Adherence KPIs</div>
            <p className="muted" style={{ marginTop: 4 }}>
              Horizon: {horizon === "week" ? "Past 7 days" : "Past 30 days"}
            </p>
          </div>
          <div className="pill soft" style={{ background: `${adherenceStatus.color}22`, color: adherenceStatus.color }}>
            {adherenceStatus.label}
          </div>
        </div>
        <div className="kpi-grid compact three">
          <article className="kpi-card small">
            <div className="kpi-title">Overall Adherence</div>
            <div className="kpi-value" style={{ color: adherenceStatus.color }}>
              {dashboard ? `${dashboard.adherence.overall_adherence_rate}%` : "--"}
            </div>
            <p className="muted" style={{ margin: 0, fontSize: 12 }}>Total doses taken (on-time + late).</p>
          </article>
          <article className="kpi-card small">
            <div className="kpi-title">On-time Rate</div>
            <div className="kpi-value small">{dashboard ? `${dashboard.adherence.on_time_rate}%` : "--"}</div>
            <p className="muted" style={{ margin: 0, fontSize: 12 }}>Punctuality for time-sensitive meds.</p>
          </article>
          <article className="kpi-card small">
            <div className="kpi-title">Missed Doses</div>
            <div className="kpi-value small">{dashboard ? dashboard.adherence.missed_doses : "-"}</div>
            <p className="muted" style={{ margin: 0, fontSize: 12 }}>{horizon === "week" ? "This week" : "This month"}</p>
          </article>
        </div>
      </section>

      <section className="card kpi-section compact">
        <div className="kpi-header">
          <div>
            <div className="pill">Symptom Intelligence KPIs (AI)</div>
            <p className="muted" style={{ marginTop: 4 }}>
              Top 3 signals in the selected horizon.
            </p>
          </div>
          <div className="pill soft" style={{ background: `${severityStatus.color}22`, color: severityStatus.color }}>
            {severityStatus.label}
          </div>
        </div>
        <div className="kpi-grid compact three">
          <article className="kpi-card small" style={{ gridColumn: "span 2" }}>
            <div className="kpi-title">Symptom Frequency & Severity</div>
            <div className="kpi-value small">{dashboard ? dashboard.symptoms.frequency : "-"}</div>
            <p className="muted" style={{ margin: 0, fontSize: 12 }}>{horizon === "week" ? "Logged this week" : "Logged this month"}</p>
            <div className="label" style={{ marginTop: 6 }}>Top trending</div>
            {trendingSymptoms.length ? (
              <ul className="trend-list">
                {trendingSymptoms.map((sym) => (
                  <li key={sym.symptom}>
                    <span>{sym.symptom}</span>
                    <strong>{sym.count}x</strong>
                  </li>
                ))}
              </ul>
            ) : (
              <span className="muted">No trending symptoms</span>
            )}
            {severityLabels.length ? (
              <div style={{ marginTop: 10 }}>
                <StackedBar labels={severityLabels} data={severityData} height={160} />
              </div>
            ) : (
              <span className="muted">No severity data for this horizon</span>
            )}
          </article>
          <article className="kpi-card small">
            <div className="kpi-title">New Symptoms</div>
            {dashboard && newSymptoms.length > 0 ? (
              <ul className="trend-list">
                {newSymptoms.map((item) => (
                  <li key={`${item.symptom}-${item.first_seen}`}>
                    <span>! {item.symptom}</span>
                    <span className="muted">{formatDate(item.first_seen)}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <span className="muted">No new symptoms</span>
            )}
          </article>
        </div>
      </section>
    </main>
  );
}
