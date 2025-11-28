"use client";

import { useEffect, useMemo, useState } from "react";
import { clearEdgeMessages, createEdgeMessage, listEdgeMessages } from "../../../lib/api";
import type { EdgeMessage, EdgeMessageList } from "../../../lib/types";

const DEFAULT_DEVICE_ID = "MM-BOX-AN-001";
const DEFAULT_PATIENT_NAME = "Asha Pillai";

const formatTime = (iso?: string) => (iso ? new Date(iso).toLocaleString("en-US") : "-");

function generateReply(prompt: string) {
  const trimmed = prompt.slice(0, 140);
  const templates = [
    `I hear you: "${trimmed}". Take a short rest and I will notify your doctor.`,
    `Got it: "${trimmed}". Monitor how you feel in the next hour and keep water nearby.`,
    `Noted: "${trimmed}". If it worsens, contact care immediately; I will log this now.`,
    `Thanks for telling me: "${trimmed}". I'm syncing this to your care team and suggesting rest.`,
    `Understood: "${trimmed}". Please sit down, breathe slowly, and I'll alert your doctor.`
  ];
  const idx = Math.floor(Math.random() * templates.length);
  return templates[idx];
}

export default function SymptomAnalytics() {
  const [messages, setMessages] = useState<EdgeMessage[]>([]);
  const [patientName, setPatientName] = useState(DEFAULT_PATIENT_NAME);
  const [patientId, setPatientId] = useState<string | null>(null);
  const [incomingText, setIncomingText] = useState("");
  const [replyPreview, setReplyPreview] = useState("");
  const [sendingState, setSendingState] = useState<"idle" | "receiving" | "replying" | "sent">("idle");
  const [error, setError] = useState<string | null>(null);

  const loadMessages = async () => {
    try {
      const res: EdgeMessageList = await listEdgeMessages();
      setMessages(res.messages);
      setPatientName(res.patient_name || DEFAULT_PATIENT_NAME);
      setPatientId(res.patient_id);
    } catch (err) {
      setError("Could not load messages");
    }
  };

  useEffect(() => {
    loadMessages();
  }, []);

  const handleReceive = async () => {
    if (!incomingText.trim()) return;
    setError(null);
    setSendingState("receiving");
    try {
      await createEdgeMessage({
        patient_id: patientId || undefined,
        device_id: DEFAULT_DEVICE_ID,
        speaker: "Patient",
        direction: "IN",
        content: incomingText.trim()
      });
      setIncomingText("");
      await loadMessages();
      setSendingState("replying");
      const reply = generateReply(incomingText.trim());
      setReplyPreview(reply);
      await new Promise((resolve) => setTimeout(resolve, 600));
      await createEdgeMessage({
        patient_id: patientId || undefined,
        device_id: DEFAULT_DEVICE_ID,
        speaker: "Assistant",
        direction: "OUT",
        content: reply
      });
      await loadMessages();
      setSendingState("sent");
      setTimeout(() => setSendingState("idle"), 800);
    } catch (err) {
      setError("Failed to send/receive. Please try again.");
      setSendingState("idle");
    }
  };

  const recentMessages = useMemo(() => messages.slice(0, 8), [messages]);

  const handleClear = async () => {
    if (!patientId) return;
    setError(null);
    try {
      await clearEdgeMessages(patientId);
      await loadMessages();
      setReplyPreview("");
    } catch (err) {
      setError("Failed to clear messages.");
    }
  };

  return (
    <main className="doctor-page" style={{ gap: 16 }}>
      <section className="card" style={{ display: "grid", gap: 14 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div className="pill">Symptom Conversation Bridge</div>
            <h3 style={{ margin: "6px 0 0" }}>{patientName}</h3>
            <div className="muted" style={{ fontSize: 13 }}>Edge raw text → server → response back to device.</div>
          </div>
          <div className="pill" style={{ background: "#ecfeff", color: "#0f766e" }}>Default patient</div>
        </div>
        <div className="chat-grid">
          <div className="chat-pane">
            <div className="label">Edge → Server (raw text)</div>
            <textarea
              value={incomingText}
              onChange={(e) => setIncomingText(e.target.value)}
              placeholder="Type raw symptom text from the edge device..."
              rows={4}
            />
            <button className="primary-btn" onClick={handleReceive} disabled={sendingState === "receiving" || sendingState === "replying"}>
              {sendingState === "receiving" ? "Receiving..." : "Mark as received"}
            </button>
            <div className="muted" style={{ fontSize: 12, marginTop: 6 }}>
              Device: {DEFAULT_DEVICE_ID}
            </div>
          </div>
          <div className="chat-pane">
            <div className="label">Server → Device (auto reply)</div>
            <div className="reply-box">
              <div className="muted" style={{ fontSize: 12, marginBottom: 6 }}>
                {sendingState === "replying" ? "Generating quick reply..." : sendingState === "sent" ? "Sent" : "Ready"}
              </div>
              <p style={{ margin: 0, minHeight: 60 }}>{replyPreview || "Reply will appear here after receiving."}</p>
            </div>
            <div className="status-row">
              <span className="status-dot" style={{ background: sendingState === "sent" ? "var(--success)" : "var(--warning)" }} />
              <span className="muted" style={{ fontSize: 12 }}>
                {sendingState === "replying"
                  ? "Sending..."
                  : sendingState === "sent"
                  ? "Reply sent back to device"
                  : "Awaiting incoming text"}
              </span>
            </div>
          </div>
        </div>
        {error && <div className="pill soft" style={{ background: "#fef2f2", color: "#b91c1c" }}>{error}</div>}
      </section>

      <section className="card" style={{ display: "grid", gap: 10 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 10 }}>
          <div>
            <div className="pill">Edge Text Storage</div>
            <div className="muted" style={{ fontSize: 13 }}>Latest raw text and responses captured for analytics.</div>
          </div>
          <button className="ghost-pill danger" onClick={handleClear} disabled={!patientId || messages.length === 0}>
            Clear storage
          </button>
        </div>
        <div className="table">
          <div className="table-head">
            <span>Direction</span>
            <span>Speaker</span>
            <span>Device</span>
            <span>Timestamp</span>
            <span>Content</span>
          </div>
          {recentMessages.map((m) => (
            <div key={m.id} className="table-row">
              <span className={`pill soft ${m.direction === "IN" ? "info" : "warning"}`}>{m.direction === "IN" ? "Edge → Server" : "Server → Edge"}</span>
              <span>{m.speaker || "-"}</span>
              <span className="muted">{m.device_id || "-"}</span>
              <span className="muted">{formatTime(m.created_at)}</span>
              <span>{m.content}</span>
            </div>
          ))}
          {!recentMessages.length && <div className="muted">No messages yet.</div>}
        </div>
      </section>
    </main>
  );
}
