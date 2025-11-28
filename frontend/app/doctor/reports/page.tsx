const reports = [
  { type: "Weekly", patient: "Minh An Bui", period: "2024-05-20 to 2024-05-26", url: "#" },
  { type: "Monthly", patient: "Van B Tran", period: "May 2024", url: "#" }
];

export default function Reports() {
  return (
    <main className="doctor-page">
      <section className="card">
        <div className="pill">Reports</div>
        <div className="grid" style={{ gap: 8 }}>
          {reports.map((r) => (
            <div key={r.period} className="card" style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <strong>{r.type}</strong> - {r.patient}
                <div className="muted">{r.period}</div>
              </div>
              <a href={r.url} className="pill">Download</a>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
