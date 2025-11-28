import type { DoseEvent } from "../lib/types";

const statusColor: Record<DoseEvent["status"], string> = {
  ON_TIME: "var(--success)",
  LATE: "var(--warning)",
  MISSED: "var(--danger)"
};

export default function Timeline({ events }: { events: DoseEvent[] }) {
  return (
    <section className="card">
      <h3 className="section-title">Today&apos;s dose log</h3>
      <div className="grid">
        {events.map((ev) => (
          <div key={ev.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div style={{ fontWeight: 600 }}>{ev.label}</div>
              <div className="muted" style={{ fontSize: 12 }}>
                {ev.time}
              </div>
            </div>
            <span className="pill" style={{ background: `${statusColor[ev.status]}22`, color: statusColor[ev.status] }}>
              {ev.status}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
