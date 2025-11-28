import "../../styles/admin.css";
import SidebarNav from "../../components/SidebarNav";
import Topbar from "../../components/Topbar";
import type { Route } from "next";

const groups = [
  {
    label: "Dashboard",
    items: [{ href: "/admin/dashboard", label: "Dashboard" }]
  },
  {
    label: "Devices",
    items: [
      { href: "/admin/devices", label: "Devices" },
      { href: "/admin/device-events", label: "Device Events" }
    ]
  },
  {
    label: "Accounts",
    items: [
      { href: "/admin/users", label: "Users" },
      { href: "/admin/patients", label: "Patients" }
    ]
  },
  {
    label: "Monitoring",
    items: [
      { href: "/admin/logs", label: "Logs" },
      { href: "/admin/system-health", label: "System Health" },
      { href: "/admin/settings", label: "Settings" }
    ]
  }
] satisfies { label: string; items: { href: Route; label: string }[] }[];

export const metadata = { title: "Admin Portal" };

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <Topbar persona="Admin" name="Admin MedMind" role="Admin" />
      <div className="app-body">
        <SidebarNav groups={groups} title="Admin" />
        <div className="content">{children}</div>
      </div>
    </div>
  );
}
