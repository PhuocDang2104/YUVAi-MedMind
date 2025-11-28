const metrics = [
  { title: "API uptime", value: "99.9%", desc: "Last 7 days" },
  { title: "LLM latency p95", value: "1.2s", desc: "Voice -> intent pipeline" },
  { title: "Queue backlog", value: "3 jobs", desc: "voice/notification" },
  { title: "Device online", value: "24/28", desc: "Paired devices" }
];

const charts = [
  { title: "API error rate", note: "5xx / minute (placeholder chart)" },
  { title: "LLM latency trend", note: "Latency p50/p95 (placeholder chart)" },
  { title: "Device heartbeat", note: "Online/offline by hour (placeholder chart)" }
];

export default function AdminDashboard() {
  return (
    <main className="admin-page">
      <section className="metric-grid">
        {metrics.map((m) => (
          <article key={m.title} className="card">
            <div className="pill">{m.title}</div>
            <h2 style={{ margin: "6px 0" }}>{m.value}</h2>
            <div className="muted">{m.desc}</div>
          </article>
        ))}
      </section>

      <section className="grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: 12 }}>
        {charts.map((c) => (
          <article key={c.title} className="card">
            <div className="pill">{c.title}</div>
            <div className="chart-placeholder">{c.note}</div>
          </article>
        ))}
      </section>
    </main>
  );
}
