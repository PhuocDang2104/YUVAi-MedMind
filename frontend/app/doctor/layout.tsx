import "../../styles/doctor.css";
import SidebarNav from "../../components/SidebarNav";
import Topbar from "../../components/Topbar";
import type { Route } from "next";

const groups = [
  {
    label: "Dashboard",
    items: [
      { href: "/doctor/dashboard/overall", label: "Overall" },
      { href: "/doctor/dashboard/patient", label: "Patient Dashboard" },
      { href: "/doctor/dashboard/alerts", label: "Alert Center" }
    ]
  },
  {
    label: "Patients",
    items: [
      { href: "/doctor/patients", label: "Patients" },
      { href: "/doctor/medication-plans", label: "Medication Plans" }
    ]
  },
  {
    label: "Analytics",
    items: [
      { href: "/doctor/symptom-analytics", label: "Symptom Analytics" },
      { href: "/doctor/ai-insights", label: "AI Insights" },
      { href: "/doctor/reports", label: "Reports" }
    ]
  }
] satisfies { label: string; items: { href: Route; label: string }[] }[];

export const metadata = { title: "Doctor Portal" };

export default function DoctorLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <Topbar persona="Doctor" name="Dr. Le Hai" role="Doctor" />
      <div className="app-body">
        <SidebarNav groups={groups} title="Doctor" />
        <div className="content">{children}</div>
      </div>
    </div>
  );
}
