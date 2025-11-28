const metrics = [
  { name: "Redis stream status", value: "OK" },
  { name: "LLM latency", value: "1200 ms" },
  { name: "API uptime", value: "99.9%" },
  { name: "Storage usage", value: "35%" }
];

export default function SystemHealth() {
  return (
    <main className="admin-page" style={{ gap: 12 }}>
      {metrics.map((m) => (
        <article key={m.name} className="card">
          <div className="pill">{m.name}</div>
          <h3 style={{ margin: "6px 0" }}>{m.value}</h3>
        </article>
      ))}
    </main>
  );
}
