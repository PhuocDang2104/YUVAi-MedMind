"use client";

import { useEffect, useMemo, useState } from "react";
import { getDoctorOverview } from "../../../../lib/api";
import type { DoctorOverview } from "../../../../lib/types";

export default function DoctorAlertsDashboard() {
  const [overview, setOverview] = useState<DoctorOverview | null>(null);

  useEffect(() => {
    getDoctorOverview().then(setOverview).catch(() => {});
  }, []);

  const alerts = overview?.alerts ?? [];
  const counts = useMemo(() => {
    return alerts.reduce(
      (acc, cur) => {
        const level = cur.level?.toLowerCase() || "info";
        if (level.includes("high") || level.includes("critical")) acc.high += 1;
        else if (level.includes("medium")) acc.medium += 1;
        else acc.low += 1;
        return acc;
      },
      { high: 0, medium: 0, low: 0 }
    );
  }, [alerts]);
  const formatTime = (value?: string) => (value ? new Date(value).toLocaleString("en-US") : "-");
  const levelStyle = (level?: string) => {
    const key = level?.toLowerCase() || "info";
    if (key.includes("high") || key.includes("critical")) {
      return { bg: "#fef2f2", color: "#b91c1c", dot: "#ef4444" };
    }
    if (key.includes("medium")) {
      return { bg: "#fff7ed", color: "#c2410c", dot: "#f97316" };
    }
    return { bg: "#ecfeff", color: "#0f766e", dot: "#0ea5e9" };
  };

  return (
    <main className="doctor-page">
      <section className="card">
        <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
          <div>
            <div className="pill">Alert center</div>
            <div className="muted" style={{ marginTop: 6 }}>Monitor patient critical signals in real time.</div>
          </div>
          <div className="alert-summary">
            <div className="badge badge-soft danger">High: {counts.high}</div>
            <div className="badge badge-soft warning">Medium: {counts.medium}</div>
            <div className="badge badge-soft info">Other: {counts.low}</div>
          </div>
        </div>

        {alerts.length ? (
          <div className="alert-list">
            {alerts.map((a, idx) => {
              const styles = levelStyle(a.level);
              return (
                <div key={idx} className="alert-item">
                  <div className="alert-dot" style={{ background: styles.dot }} />
                  <div className="alert-body">
                    <div className="alert-title-row">
                      <div style={{ fontWeight: 600 }}>{a.message}</div>
                    <div className="badge" style={{ background: styles.bg, color: styles.color }}>{a.level || "Info"}</div>
                  </div>
                  <div className="alert-meta">
                    <span>{formatTime(a.time)}</span>
                    <span>Flag and reach out now</span>
                  </div>
                </div>
              </div>
            );
          })}
          </div>
        ) : (
          <div className="muted">No alerts</div>
        )}
      </section>
    </main>
  );
}
