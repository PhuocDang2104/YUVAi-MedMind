"use client";

import { useEffect, useState } from "react";
import { getDoctorPatients, getPatientMedicationPlan } from "../../../lib/api";
import type { DoctorPatient, PatientMedicationPlan } from "../../../lib/types";

export default function MedicationPlans() {
  const [patients, setPatients] = useState<DoctorPatient[]>([]);
  const [plan, setPlan] = useState<PatientMedicationPlan | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const doses = plan?.doses || [];

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
      getPatientMedicationPlan(selected).then(setPlan).catch(() => {});
    }
  }, [selected]);

  return (
    <main className="doctor-page">
      <section className="card">
        <div className="pill">Select patient</div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 8 }}>
          {patients.map((p) => (
            <button
              key={p.id}
              onClick={() => setSelected(p.id)}
              style={{
                padding: "8px 12px",
                borderRadius: 10,
                border: selected === p.id ? "1px solid var(--primary)" : "1px solid var(--border)",
                background: selected === p.id ? "rgba(37,99,235,0.08)" : "#fff",
                cursor: "pointer"
              }}
            >
              {p.name}
            </button>
          ))}
        </div>
      </section>

      <section className="card">
        <div className="pill">Doses today</div>
        <div className="grid" style={{ gap: 8 }}>
          <div className="muted" style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1fr", fontWeight: 600 }}>
            <span>Medication</span><span>Dose</span><span>Time</span><span>Status / Symptom</span>
          </div>
          {doses.length ? (
            doses.map((d, idx) => (
              <div key={idx} className="card" style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1fr", alignItems: "center" }}>
                <span>{d.med_name}</span>
                <span>{d.dose}</span>
                <span>{new Date(d.time).toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })}</span>
                <span>{d.status} {d.symptom ? `- ${d.symptom}` : ""}</span>
              </div>
            ))
          ) : (
            <div className="muted">Select a patient to view the medication plan.</div>
          )}
        </div>
      </section>
    </main>
  );
}
