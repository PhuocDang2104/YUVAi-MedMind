const insights = [
  {
    title: "Adherence Pattern",
    summary: "Evening doses are missed more often on weekends, especially the Amlodipine slot.",
    impact: "Higher risk of nighttime hypertension and poorer sleep quality.",
    actions: ["Call before 20:00", "Move to morning slot for this week", "Send push notification to caregiver"],
    confidence: "High",
    timeScope: "Current week"
  },
  {
    title: "Symptom-Medication Correlation",
    summary: "Dizziness appears after skipping evening Metformin.",
    impact: "May raise fasting glucose the next morning; monitor glucose.",
    actions: ["Recommend morning glucose check", "Remind to take Metformin before bedtime"],
    confidence: "Medium",
    timeScope: "Last 3 days"
  },
  {
    title: "Risk Signal",
    summary: "Shortness of breath + chest pain occurred once; risk level HIGH.",
    impact: "Potential cardiac event risk; needs close monitoring.",
    actions: ["Prioritize push to caregiver", "Ask to call doctor if it repeats", "Flag alert as critical"],
    confidence: "High",
    timeScope: "Past 24h"
  }
];

export default function AIInsights() {
  return (
    <main className="doctor-page" style={{ gap: 12 }}>
      {insights.map((i) => (
        <article key={i.title} className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div className="pill">{i.title}</div>
            <span className="pill" style={{ background: "rgba(37,99,235,0.12)" }}>
              {i.timeScope}
            </span>
          </div>
          <p style={{ margin: "8px 0", fontWeight: 600 }}>{i.summary}</p>
          <div className="muted" style={{ marginBottom: 6 }}>Impact: {i.impact}</div>
          <div className="muted" style={{ marginBottom: 8 }}>Confidence: {i.confidence}</div>
          <div className="muted" style={{ fontSize: 13, marginBottom: 6 }}>Suggested actions:</div>
          <ul style={{ margin: 0, paddingLeft: 18, color: "var(--text)" }}>
            {i.actions.map((a) => (
              <li key={a} style={{ marginBottom: 4 }}>{a}</li>
            ))}
          </ul>
        </article>
      ))}
    </main>
  );
}
