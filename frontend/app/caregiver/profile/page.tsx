export default function Profile() {
  return (
    <main className="caregiver-page">
      <section className="card">
        <div className="pill">Caregiver</div>
        <h3 style={{ margin: "6px 0" }}>Thao Nguyen</h3>
        <div className="muted">caregiver@example.com</div>
      </section>
      <section className="card">
        <div className="pill">Patient</div>
        <h3 style={{ margin: "6px 0" }}>Minh An Bui</h3>
        <div className="muted">Hypertension, T2D</div>
        <div className="muted">Paired device: MM-BOX-001</div>
      </section>
      <section className="card">
        <div className="pill">Settings</div>
        <div className="grid" style={{ gap: 8 }}>
          {["Pair/unpair device", "Notification settings", "Download health reports", "Logout"].map((s) => (
            <button key={s} style={{ padding: "10px 12px", borderRadius: 10, border: "1px solid rgba(255,255,255,0.1)", background: "transparent", color: "inherit", cursor: "pointer" }}>
              {s}
            </button>
          ))}
        </div>
      </section>
    </main>
  );
}
