const devices = [
  { uid: "MM-BOX-001", patient: "Minh An Bui", status: "Online", firmware: "1.0.0", lastSeen: "Just now" }
];

export default function Devices() {
  return (
    <main className="admin-page">
      <section className="card">
        <div className="pill">Devices</div>
        <div className="grid" style={{ gap: 8 }}>
          <div className="muted" style={{ display: "grid", gridTemplateColumns: "repeat(5, minmax(0,1fr))", fontWeight: 600 }}>
            <span>UID</span><span>Patient</span><span>Status</span><span>Firmware</span><span>Last Seen</span>
          </div>
          {devices.map((d) => (
            <div key={d.uid} className="card" style={{ display: "grid", gridTemplateColumns: "repeat(5, minmax(0,1fr))", gap: 6, alignItems: "center" }}>
              <span>{d.uid}</span>
              <span>{d.patient}</span>
              <span>{d.status}</span>
              <span>{d.firmware}</span>
              <span>{d.lastSeen}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
