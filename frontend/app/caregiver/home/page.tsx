const overview = {
  total: "8/10 doses taken",
  onTime: 6,
  late: 1,
  missed: 1
};

const upcoming = { time: "21:00", label: "Metformin 500mg", status: "Coming up" };
const symptoms = [
  { time: "09:32", text: "Headache, dizziness", severity: "Medium" },
  { time: "Yesterday", text: "Trouble sleeping", severity: "Mild" }
];

export default function CaregiverHome() {
  return (
    <main className="caregiver-page">
      <section className="card">
        <div className="pill">Today Overview</div>
        <h2 style={{ margin: "6px 0" }}>{overview.total}</h2>
        <div className="caregiver-stats">
          <div className="pill" style={{ background: "rgba(52,211,153,0.12)" }}>On time: {overview.onTime}</div>
          <div className="pill" style={{ background: "rgba(251,191,36,0.12)" }}>Late: {overview.late}</div>
          <div className="pill" style={{ background: "rgba(248,113,113,0.12)" }}>Missed: {overview.missed}</div>
        </div>
      </section>

      <section className="caregiver-columns">
        <article className="card">
          <div className="pill">Upcoming Dose</div>
          <h3 style={{ margin: "6px 0" }}>{upcoming.time} - {upcoming.label}</h3>
          <div className="muted">{upcoming.status}</div>
        </article>

        <article className="card">
          <div className="pill">Device Status</div>
          <div className="muted">Online - Battery 85% - 34C - FW 1.0.0</div>
        </article>

        <article className="card">
          <div className="pill">Quick Actions</div>
          <div className="caregiver-actions">
            {["Sync schedule", "Call patient", "Add manual log"].map((act) => (
              <button key={act} style={{ padding: "10px 12px", borderRadius: 10, border: "1px solid rgba(255,255,255,0.1)", background: "transparent", color: "inherit", cursor: "pointer" }}>
                {act}
              </button>
            ))}
          </div>
        </article>
      </section>

      <section className="card">
        <div className="pill">Recent Symptoms</div>
        <div className="grid" style={{ gap: 10 }}>
          {symptoms.map((s) => (
            <div key={s.text} style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <strong>{s.time}</strong> - {s.text}
              </div>
              <span className="pill" style={{ background: "rgba(192,132,252,0.16)" }}>Level: {s.severity}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
