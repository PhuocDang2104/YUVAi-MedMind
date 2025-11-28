import StatusCards from "../../components/StatusCards";
import Timeline from "../../components/Timeline";
import type { DoseEvent } from "../../lib/types";

const mockEvents: DoseEvent[] = [
  { id: "1", label: "Blood pressure - morning", status: "ON_TIME", time: "08:00" },
  { id: "2", label: "Diabetes - noon", status: "LATE", time: "12:30" },
  { id: "3", label: "Blood pressure - evening", status: "MISSED", time: "20:00" }
];

export default function Dashboard() {
  return (
    <main className="grid" style={{ gap: 18 }}>
      <StatusCards />
      <Timeline events={mockEvents} />
    </main>
  );
}
