"use client";

import { useEffect, useMemo, useState } from "react";
import { getDoctorOverview } from "../../../../lib/api";
import type { DoctorOverview } from "../../../../lib/types";
import dynamic from "next/dynamic";

const LineChart = dynamic(() => import("../../../../components/LineChart"), { ssr: false });
const StackedBar = dynamic(() => import("../../../../components/StackedBar"), { ssr: false });

export default function DoctorOverallDashboard() {
  const [overview, setOverview] = useState<DoctorOverview | null>(null);
  const [selectedNotification, setSelectedNotification] = useState<string | null>(null);

  useEffect(() => {
    getDoctorOverview().then(setOverview).catch(() => {});
  }, []);

  const metrics = useMemo(() => overview?.metrics, [overview]);
  const adherenceLabels = useMemo(() => overview?.adherence_trend.map((p) => p.label) || [], [overview]);
  const adherenceValues = useMemo(() => overview?.adherence_trend.map((p) => p.value) || [], [overview]);
  const symptomLabels = useMemo(() => overview?.symptom_by_patient.labels || [], [overview]);
  const symptomSeries = useMemo(() => overview?.symptom_by_patient.series || [], [overview]);
  const notifications = useMemo(() => overview?.ai_notifications || [], [overview]);
  useEffect(() => {
    if (notifications.length && !selectedNotification) {
      setSelectedNotification(notifications[0].patient_id);
    }
  }, [notifications, selectedNotification]);

  const currentNote = notifications.find((n) => n.patient_id === selectedNotification);
  const palette = ["#2563eb", "#f97316", "#22c55e"];

  return (
    <main className="doctor-page">
      <section className="metric-grid" style={{ gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))" }}>
        {overview && metrics && (
          <>
            <article className="card kpi-tall">
              <div className="pill">Overall Adherence</div>
              <h2 style={{ margin: "6px 0" }}>{overview.adherence_summary.mean}%</h2>
              <div className="muted" style={{ fontSize: 13 }}>
                High: {overview.adherence_summary.high_count} | Medium: {overview.adherence_summary.medium_count} | Low: {overview.adherence_summary.low_count}
              </div>
            </article>
            <article className="card kpi-tall">
              <div className="pill">On-time Rate</div>
              <h2 style={{ margin: "6px 0" }}>{overview.on_time_summary.mean}%</h2>
              <div className="muted" style={{ fontSize: 13 }}>
                High: {overview.on_time_summary.high_count} | Medium: {overview.on_time_summary.medium_count} | Low: {overview.on_time_summary.low_count}
              </div>
            </article>
            <article className="card kpi-tall">
              <div className="pill">Missed Doses</div>
              <h2 style={{ margin: "6px 0" }}>
                {overview.missed_summary.total_7d}
                <span className="muted" style={{ fontSize: 12 }}> (7d)</span>
              </h2>
              <div className="muted" style={{ fontSize: 13 }}>
                30d: {overview.missed_summary.total_30d} • Per patient/week: {overview.missed_summary.per_patient_week}
              </div>
              {overview.missed_summary.top_patients.length > 0 && (
                <ul className="kpi-list">
                  {overview.missed_summary.top_patients.map((p) => (
                    <li key={p.patient_id}>
                      {p.patient_name}: <span className="pill soft" style={{ padding: "2px 8px" }}>{p.missed_7d} missed</span>
                    </li>
                  ))}
                </ul>
              )}
            </article>
            <article className="card kpi-tall">
              <div className="pill">Symptom Frequency</div>
              <h2 style={{ margin: "6px 0" }}>
                {overview.symptom_population.total_7d}
                <span className="muted" style={{ fontSize: 12 }}> (7d)</span>
              </h2>
              <div className="muted" style={{ fontSize: 13 }}>
                30d: {overview.symptom_population.total_30d}
              </div>
              <ul className="kpi-list">
                {overview.symptom_population.top.map((t) => (
                  <li key={t.symptom}>
                    {t.symptom}: <span className="pill soft info" style={{ padding: "2px 8px" }}>{t.count}</span>
                  </li>
                ))}
              </ul>
            </article>
            <article className="card kpi-tall">
              <div className="pill">Severity Trend</div>
              <h2 style={{ margin: "6px 0" }}>
                {overview.severity_population.change_pct}% {overview.severity_population.direction === "up" ? "↑" : overview.severity_population.direction === "down" ? "↓" : "→"}
              </h2>
              <div className="muted" style={{ fontSize: 13 }}>
                Patients with higher severity: {overview.severity_population.patients_up}
              </div>
              <div className="muted" style={{ fontSize: 12, marginTop: 6 }}>
                Flagged (severe/high): {overview.severity_population.flagged_patients}
              </div>
            </article>
            <article className="card kpi-tall">
              <div className="pill">New Symptoms</div>
              <h2 style={{ margin: "6px 0" }}>{overview.new_symptoms_population.events}</h2>
              <div className="muted" style={{ fontSize: 13 }}>
                Patients: {overview.new_symptoms_population.patient_count} • Critical pts: {overview.new_symptoms_population.critical_patients}
              </div>
              <ul className="kpi-list">
                {overview.new_symptoms_population.top.map((t) => (
                  <li key={t.symptom}>
                    {t.symptom}: <span className="pill soft warning" style={{ padding: "2px 8px" }}>{t.count}</span>
                  </li>
                ))}
              </ul>
            </article>
            <article className="card kpi-tall" style={{ gridColumn: "span 2" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div>
                  <div className="pill">AI Notification</div>
                  <div className="muted" style={{ fontSize: 12 }}>Patient-specific summary</div>
                </div>
                <select value={selectedNotification || ""} onChange={(e) => setSelectedNotification(e.target.value)}>
                  {notifications.map((n) => (
                    <option key={n.patient_id} value={n.patient_id}>{n.patient_name}</option>
                  ))}
                </select>
              </div>
              <p style={{ marginTop: 8, marginBottom: 4 }}>{currentNote?.summary || "No summary"}</p>
              <textarea
                readOnly
                value={currentNote?.detail || ""}
                placeholder="AI insight summary"
                style={{ width: "100%", minHeight: 90, borderRadius: 10, border: "1px solid var(--border)", padding: "10px", resize: "vertical" }}
              />
            </article>
          </>
        )}
      </section>

      <section className="doctor-chart-split">
        <div className="card">
          <div className="pill">Adherence trend</div>
          {adherenceLabels.length ? (
            <LineChart
              labels={adherenceLabels}
              series={[{ label: "Adherence %", data: adherenceValues, color: "#2563eb" }]}
              height={140}
              showFill
            />
          ) : (
            <div className="chart-placeholder">No data</div>
          )}
        </div>
        <div className="card" style={{ display: "grid", gap: 12 }}>
          <div className="pill pill-compact">Symptom distribution by patient</div>
          {symptomLabels.length && symptomSeries.length ? (
            <div className="chart-fixed">
              <StackedBar
                labels={symptomLabels}
                data={symptomSeries.map((s, idx) => ({ label: s.label, values: s.values, color: palette[idx % palette.length] }))}
                height="100%"
              />
            </div>
          ) : (
            <div className="chart-placeholder">No data</div>
          )}
        </div>
      </section>
    </main>
  );
}
