const settings = [
  "API keys",
  "Notification templates",
  "OTA firmware channels (stable/beta)"
];

export default function Settings() {
  return (
    <main className="admin-page">
      <section className="card">
        <div className="pill">Admin Settings</div>
        <div className="grid" style={{ gap: 8 }}>
          {settings.map((s) => (
            <div key={s} className="card">
              {s}
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
