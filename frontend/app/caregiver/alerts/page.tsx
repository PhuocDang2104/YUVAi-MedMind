const critical = [
  { title: "Shortness of breath, chest pain", time: "23:14", desc: "EMERGENCY", risk: "HIGH" },
  { title: "2 evening doses were missed", time: "07:00", desc: "Medication adherence", risk: "MED" }
];

const deviceAlerts = [
  { title: "Box offline 12h", desc: "Last seen 09:00" },
  { title: "Low battery", desc: "Battery 20%" }
];

const notifLog = [
  { title: "Reminder sent", date: "Today" },
  { title: "Emergency push sent", date: "Yesterday" }
];

export default function Alerts() {
  return (
    <main className="caregiver-page">
      <section className="card">
        <div className="pill">Critical Alerts</div>
        <div className="grid" style={{ gap: 8 }}>
          {critical.map((c) => (
            <div key={c.title} className="card">
              <strong>{c.time} - {c.title}</strong>
              <div className="muted">{c.desc}</div>
              <span className="pill" style={{ background: "rgba(248,113,113,0.16)", color: "var(--danger)" }}>Risk: {c.risk}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <div className="pill">Device Alerts</div>
        <div className="grid" style={{ gap: 8 }}>
          {deviceAlerts.map((d) => (
            <div key={d.title} className="card">
              <strong>{d.title}</strong>
              <div className="muted">{d.desc}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <div className="pill">Notifications Log</div>
        <div className="grid" style={{ gap: 8 }}>
          {notifLog.map((n) => (
            <div key={n.title} className="card">
              <strong>{n.title}</strong>
              <div className="muted">{n.date}</div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
