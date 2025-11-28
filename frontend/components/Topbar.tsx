"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

type TopbarProps = {
  persona: "Caregiver" | "Doctor" | "Admin";
  name?: string;
  role?: string;
};

export default function Topbar({ persona, name = "Demo User", role }: TopbarProps) {
  const router = useRouter();
  const [query, setQuery] = useState("");

  const iconStyle: React.CSSProperties = { width: 16, height: 16, display: "inline-block", color: "#111" };

  return (
    <div className="topbar">
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{ fontWeight: 700, color: "#0f172a" }}>MedMind</div>
        <div className="muted" style={{ fontWeight: 600 }}>{persona} Portal</div>
      </div>
      <div className="search">
        <svg style={iconStyle} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="7" />
          <line x1="16.65" y1="16.65" x2="21" y2="21" />
        </svg>
        <input
          placeholder="Search patient, device, report..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <button
          style={{
            border: "1px solid var(--border)",
            background: "#f8fafc",
            padding: "8px 10px",
            borderRadius: 10,
            cursor: "pointer"
          }}
        >
          <svg style={iconStyle} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 22c1.1 0 2-.9 2-2H10a2 2 0 0 0 2 2Zm6-6V11a6 6 0 0 0-5-5.91V4a1 1 0 0 0-2 0v1.09A6 6 0 0 0 6 11v5l-2 2v1h16v-1l-2-2Z" />
          </svg>
        </button>
        <button
          style={{
            border: "1px solid var(--border)",
            background: "#f8fafc",
            padding: "8px 10px",
            borderRadius: 10,
            cursor: "pointer"
          }}
        >
          <svg style={iconStyle} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="3" />
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 8.4 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 8.4 5a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9c.18.53.27 1.09.26 1.66v.68c0 .57-.09 1.13-.26 1.66Z" />
          </svg>
        </button>
        <button
          onClick={() => router.push("/")}
          style={{
            border: "1px solid var(--border)",
            background: "#fff",
            padding: "8px 12px",
            borderRadius: 10,
            cursor: "pointer"
          }}
          title="Logout"
        >
          <svg style={iconStyle} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
        </button>
        <div
          style={{ display: "flex", alignItems: "center", gap: 10, cursor: "pointer" }}
          onClick={() => router.push("/")}
          title="Back to login"
        >
          <div style={{ textAlign: "right" }}>
            <div style={{ fontWeight: 600 }}>{name}</div>
            <div className="muted" style={{ fontSize: 12 }}>{role || persona}</div>
          </div>
          <div className="avatar">{name[0] || persona[0]}</div>
        </div>
      </div>
    </div>
  );
}
