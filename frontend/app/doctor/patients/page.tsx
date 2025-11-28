"use client";

import { useEffect, useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { getDoctorPatients, getPatientTimeline } from "../../../lib/api";
import type { DoctorPatient, PatientTimeline } from "../../../lib/types";

const LineChart = dynamic(() => import("../../../components/LineChart"), { ssr: false });

export default function Patients() {
  const [patients, setPatients] = useState<DoctorPatient[]>([]);
  const [timeline, setTimeline] = useState<PatientTimeline | null>(null);
  const [selected, setSelected] = useState<string | null>(null);

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
    if (selected) {
      getPatientTimeline(selected).then(setTimeline).catch(() => {});
    }
  }, [selected]);

  const formatDate = (value?: string | null) => (value ? new Date(value).toLocaleString("en-US") : "-");
  const chartLabels = useMemo(() => timeline?.points.map((p) => p.label) || [], [timeline]);
  const chartSeries = useMemo(
    () => (timeline ? [{ label: "Adherence %", data: timeline.points.map((p) => p.adherence), color: "#2563eb" }] : []),
    [timeline]
  );
  const markers = useMemo(
    () =>
      timeline
        ? timeline.points
            .filter((p) => p.alerts > 0)
            .map((p) => ({ x: p.label, label: `${p.alerts} alert${p.alerts > 1 ? "s" : ""}`, y: p.adherence }))
        : [],
    [timeline]
  );
  const selectedPatient = patients.find((p) => p.id === selected);

  return (
    <main className="doctor-page">
      <section className="card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 10 }}>
          <div className="pill">Patients</div>
          {selectedPatient && <div className="muted">Viewing: {selectedPatient.name}</div>}
        </div>
        <div className="grid" style={{ gap: 8 }}>
          <div className="muted" style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1fr", fontWeight: 600 }}>
            <span>Name</span>
            <span>Adherence</span>
            <span>Alerts</span>
            <span>Last Update</span>
          </div>
          {patients.map((p) => (
            <div
              key={p.id}
              className="card"
              style={{
                display: "grid",
                gridTemplateColumns: "2fr 1fr 1fr 1fr",
                cursor: "pointer",
                border: selected === p.id ? "1.5px solid var(--primary)" : "1px solid var(--border)",
                boxShadow: selected === p.id ? "0 8px 20px rgba(37,99,235,0.12)" : undefined
              }}
              onClick={() => setSelected(p.id)}
            >
              <strong>{p.name}</strong>
              <span>{p.adherence}%</span>
              <span>{p.alerts}</span>
              <span className="muted">{formatDate(p.last_update)}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
          <div className="pill">Adherence with Alerts</div>
          {selectedPatient && (
            <div className="pill" style={{ background: "#fef2f2", color: "#b91c1c" }}>
              Alerts: {selectedPatient.alerts}
            </div>
          )}
        </div>
        {chartLabels.length ? (
          <LineChart labels={chartLabels} series={chartSeries} markers={markers} height={200} />
        ) : (
          <div className="muted">Select a patient to view the chart</div>
        )}
      </section>
    </main>
  );
}
