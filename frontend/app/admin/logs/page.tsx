const tabs = ["Dose Event Logs", "Symptom Logs", "Medication Question Logs", "Alert Logs"];

export default function Logs() {
  return (
    <main className="admin-page">
      <section className="card">
        <div className="pill">Logs</div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 8 }}>
          {tabs.map((t) => (
            <span key={t} className="pill" style={{ background: "rgba(255,255,255,0.08)" }}>
              {t}
            </span>
          ))}
        </div>
        <p className="muted" style={{ marginTop: 8 }}>Viewer with device_id / event_type / time range filters (placeholder).</p>
      </section>
    </main>
  );
}
