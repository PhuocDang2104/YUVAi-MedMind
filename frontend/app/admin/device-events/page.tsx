const events = [
  { type: "BOX_OPENED", device: "MM-BOX-001", time: "08:05", detail: "slot A1" },
  { type: "DOSE_CONFIRMED", device: "MM-BOX-001", time: "08:06", detail: "dose id 123" }
];

export default function DeviceEvents() {
  return (
    <main className="admin-page">
      <section className="card">
        <div className="pill">Device Events</div>
        <div className="grid" style={{ gap: 8 }}>
          {events.map((e) => (
            <div key={e.time + e.type} className="card" style={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0,1fr))", gap: 6 }}>
              <span>{e.type}</span>
              <span>{e.device}</span>
              <span>{e.time}</span>
              <span className="muted">{e.detail}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
