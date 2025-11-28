"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import type { Route } from "next";

type Persona = "CAREGIVER" | "DOCTOR" | "ADMIN";

const personaCopy: Record<Persona, { title: string; desc: string; goto: Route }> = {
  CAREGIVER: {
    title: "Caregiver App (Mobile)",
    desc: "Track schedule, symptoms, alerts, and device status.",
    goto: "/caregiver/home"
  },
  DOCTOR: {
    title: "Doctor Portal (Web)",
    desc: "Patient dashboard, adherence trends, symptom analytics, AI insights.",
    goto: "/doctor/dashboard"
  },
  ADMIN: {
    title: "Admin / CS Portal",
    desc: "Manage devices, users, logs, and system health.",
    goto: "/admin/devices"
  }
};

const personaIconClass: Record<Persona, string> = {
  CAREGIVER: "bi-heart-pulse-fill",
  DOCTOR: "bi-clipboard-data-fill",
  ADMIN: "bi-tools"
};

const personaBackground: Record<Persona, string> = {
  CAREGIVER: "/persona-caregiver.jpg",
  DOCTOR: "/persona-doctor.jpg",
  ADMIN: "/persona-admin.jpg"
};

export default function Login() {
  const router = useRouter();
  const [persona, setPersona] = useState<Persona>("CAREGIVER");
  const [email, setEmail] = useState("caregiver@example.com");
  const [password, setPassword] = useState("password");

  const hero = useMemo(() => personaCopy[persona], [persona]);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    router.push(hero.goto);
  };

  return (
    <main
      className="grid"
      style={{
        gap: 24,
        placeItems: "center",
        minHeight: "100vh",
        padding: "32px 16px",
        position: "relative",
        backgroundImage: `url('${personaBackground[persona]}')`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        backgroundAttachment: "fixed"
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "rgba(255,255,255,0.78)",
          backdropFilter: "blur(0px)"
        }}
        aria-hidden
      />
      <div style={{ position: "relative", zIndex: 1, width: "100%", display: "grid", gap: 24, placeItems: "center" }}>
        <header
          className="grid card"
          style={{
            gap: 16,
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            maxWidth: 1000,
            width: "100%"
          }}
        >
          <div className="grid" style={{ gap: 12 }}>
            <div className="pill">Welcome - Choose persona</div>
            <h1 style={{ margin: 0 }}>MedMind Portal</h1>
            <p className="muted" style={{ maxWidth: 520 }}>
              Log in and pick a mode. Each persona has its own experience - tap to preview and continue.
            </p>
            <div className="grid" style={{ gap: 12 }}>
              {(["CAREGIVER", "DOCTOR", "ADMIN"] as Persona[]).map((p) => (
                <button
                  key={p}
                  onClick={() => setPersona(p)}
                  style={{
                    textAlign: "left",
                    padding: "14px",
                    borderRadius: 14,
                    border: p === persona ? "2px solid var(--primary)" : "1px solid var(--border)",
                    background: p === persona ? "rgba(37,99,235,0.08)" : "white",
                    color: "inherit",
                    cursor: "pointer",
                    boxShadow: p === persona ? "0 14px 30px rgba(37,99,235,0.18)" : "none",
                    display: "grid",
                    gridTemplateColumns: "56px 1fr",
                    alignItems: "center",
                    gap: 14,
                    position: "relative",
                    overflow: "hidden",
                    transition: "transform 220ms ease, box-shadow 220ms ease, border 220ms ease"
                  }}
                  className={p === persona ? "persona-card active" : "persona-card"}
                >
                  <div
                    style={{
                      width: 52,
                      height: 52,
                      borderRadius: 14,
                      display: "grid",
                      placeItems: "center",
                      background: p === persona ? "linear-gradient(135deg, #dbeafe, #eef2ff)" : "#f8fafc",
                      overflow: "hidden",
                      boxShadow: p === persona ? "inset 0 0 0 1px rgba(37,99,235,0.15)" : "none",
                      transition: "transform 200ms ease"
                    }}
                    aria-hidden
                  >
                    <i className={`bi ${personaIconClass[p]}`} style={{ fontSize: 22, color: "#1e3a8a" }} />
                  </div>
                  <div>
                    <strong>{personaCopy[p].title}</strong>
                    <div className="muted" style={{ fontSize: 13 }}>{personaCopy[p].desc}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>

        <form className="card" onSubmit={onSubmit} style={{ gap: 12, display: "grid", alignSelf: "stretch" }}>
          <h3 className="section-title">Sign in</h3>
          <label className="muted" style={{ display: "grid", gap: 6 }}>
            Email
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{
                padding: "12px",
                borderRadius: 10,
                border: "1px solid var(--border)",
                background: "#f8fafc",
                color: "var(--text)"
              }}
            />
          </label>
          <label className="muted" style={{ display: "grid", gap: 6 }}>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{
                padding: "12px",
                borderRadius: 10,
                border: "1px solid var(--border)",
                background: "#f8fafc",
                color: "var(--text)"
              }}
            />
          </label>
          <button
            type="submit"
            style={{
              padding: "12px",
              borderRadius: 10,
              border: "none",
              background: "linear-gradient(90deg, #2563eb, #7c3aed)",
              color: "white",
              fontWeight: 700,
              cursor: "pointer",
              boxShadow: "0 10px 30px rgba(37,99,235,0.25)"
            }}
          >
            Log in as {hero.title}
          </button>
          <div className="muted" style={{ fontSize: 12 }}>
            Demo: `caregiver@example.com`, `doctor@example.com`, `admin@example.com` (password placeholder).
          </div>
        </form>
        </header>
      </div>
    </main>
  );
}
