const filters = ["All", "Symptoms", "Questions", "Emergency", "Notes"];

const timeline = [
  { type: "Symptom", time: "09:32", title: "Headache, dizziness", severity: "Medium", context: "After waking up" },
  { type: "Medication Question", time: "20:05", title: "Can I take Metformin after dinner?", answer: "Yes, recommended after dinner." },
  { type: "Emergency", time: "23:14", title: "Shortness of breath, chest pain", risk: "HIGH" }
];

export default function HealthLog() {
  return (
    <main className="caregiver-page">
      <div className="card">
        <div className="pill">Filter</div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 8 }}>
          {filters.map((f) => (
            <span key={f} className="pill" style={{ background: "rgba(255,255,255,0.06)" }}>
              {f}
            </span>
          ))}
        </div>
      </div>
      <section className="grid" style={{ gap: 10 }}>
        {timeline.map((item) => (
          <article key={item.title} className="card">
            <div className="pill">{item.type}</div>
            <h4 style={{ margin: "6px 0" }}>{item.time} - {item.title}</h4>
            {item.severity && <div className="muted">Severity: {item.severity}</div>}
            {item.context && <div className="muted">Context: {item.context}</div>}
            {item.answer && <div className="muted">AI Answer: {item.answer}</div>}
            {item.risk && <span className="pill" style={{ background: "rgba(248,113,113,0.16)", color: "var(--danger)" }}>Risk: {item.risk}</span>}
          </article>
        ))}
      </section>
    </main>
  );
}
