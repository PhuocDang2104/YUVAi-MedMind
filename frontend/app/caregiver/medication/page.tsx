const meds = [
  { name: "Amlodipine", dose: "1 pill", freq: "Morning/Evening", slot: "A1" },
  { name: "Metformin", dose: "1 pill", freq: "Morning/Evening", slot: "B1" }
];

const weekly = [
  { day: "Mon", morning: "ON_TIME", evening: "MISSED" },
  { day: "Tue", morning: "ON_TIME", evening: "SCHEDULED" },
  { day: "Wed", morning: "LATE", evening: "ON_TIME" }
];

const statusColor: Record<string, string> = {
  ON_TIME: "rgba(52,211,153,0.2)",
  LATE: "rgba(251,191,36,0.2)",
  MISSED: "rgba(248,113,113,0.2)",
  SCHEDULED: "rgba(192,132,252,0.2)"
};

export default function Medication() {
  return (
    <main className="caregiver-page">
      <section className="card">
        <div className="pill">Active Medication Plan</div>
        <div className="grid" style={{ gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: 10 }}>
          {meds.map((m) => (
            <article key={m.name} className="card">
              <h4 style={{ margin: "6px 0" }}>{m.name}</h4>
              <div className="muted">Dose: {m.dose}</div>
              <div className="muted">Frequency: {m.freq}</div>
              <div className="muted">Slot: {m.slot}</div>
            </article>
          ))}
        </div>
      </section>

      <section className="card">
        <div className="pill">Weekly Schedule</div>
        <div className="grid" style={{ gap: 6 }}>
          {weekly.map((d) => (
            <div key={d.day} style={{ display: "grid", gridTemplateColumns: "80px 1fr 1fr", gap: 8, alignItems: "center" }}>
              <strong>{d.day}</strong>
              <span className="pill" style={{ background: statusColor[d.morning] }}>Morning: {d.morning}</span>
              <span className="pill" style={{ background: statusColor[d.evening] }}>Evening: {d.evening}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <div className="pill">Add/Modify Plan</div>
        <p className="muted">3-step wizard: pick meds -> set dose & frequency -> map to pill slots.</p>
        <button style={{ padding: "10px 12px", borderRadius: 10, border: "1px solid rgba(255,255,255,0.1)", background: "transparent", color: "inherit", cursor: "pointer" }}>
          Open wizard
        </button>
      </section>
    </main>
  );
}
