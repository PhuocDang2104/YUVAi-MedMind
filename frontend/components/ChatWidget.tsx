"use client";

import { useMemo, useState } from "react";
import { sendAIChat } from "../lib/api";
import type { AIChatMode, AIChatReport, AIChatResponse } from "../lib/types";

type ChatEntry = {
  role: "user" | "assistant";
  content: string;
  mode?: AIChatMode;
  layer?: number;
  warning?: boolean;
  report?: AIChatReport | null;
};

const patientName = "Asha Pillai";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [loadingMode, setLoadingMode] = useState<AIChatMode | null>(null);
  const [draft, setDraft] = useState("Summarize the patient status");
  const [messages, setMessages] = useState<ChatEntry[]>([
    {
      role: "assistant",
      content: "Hi, I’m MedMind AI for doctors. You can ask: “Summarize the patient status” or “Any clinical suggestions?”",
    },
  ]);

  const detectMode = (question: string): AIChatMode => {
    const q = question.toLowerCase();
    if (q.includes("suggest") || q.includes("recommend") || q.includes("advice")) return "suggestion";
    return "summary";
  };

  const ask = async (question: string) => {
    const trimmed = question.trim();
    if (!trimmed) return;
    const mode = detectMode(trimmed);
    setMessages((prev) => [...prev, { role: "user", content: trimmed, mode }]);
    setLoadingMode(mode);
    try {
      const res: AIChatResponse = await sendAIChat({ question: trimmed, mode });
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.message,
          mode: res.mode,
          layer: res.layer,
          warning: res.warning_flag || false,
          report: res.report || null,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Không gọi được trợ lý AI. Vui lòng thử lại.", mode },
      ]);
    } finally {
      setLoadingMode(null);
    }
  };

  const statusText = useMemo(() => {
    if (!loadingMode) return "Ready";
    return loadingMode === "summary" ? "Summarizing..." : "Generating suggestion...";
  }, [loadingMode]);

  const onSubmit = () => ask(draft);

  const onKeyDown: React.KeyboardEventHandler<HTMLTextAreaElement> = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <>
      <button className="chat-launcher" aria-label="Open AI chat" onClick={() => setOpen(true)}>
        <i className="bi bi-robot" />
        <span>MedMind AI</span>
      </button>

      {open && (
        <div className="chat-modal">
          <div className="chat-header">
            <div>
              <div className="chat-title">
                <i className="bi bi-heart-pulse" /> MedMind Copilot
              </div>
              <div className="chat-subtitle">Default patient: {patientName}</div>
            </div>
            <button className="ghost-btn" onClick={() => setOpen(false)}>
              <i className="bi bi-x-lg" />
            </button>
          </div>

          <div className="chat-toolbar">
            <span className="chat-status">{statusText}</span>
          </div>

          <div className="chat-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-bubble ${msg.role}`}>
                <div className="chat-meta">
                  {msg.role === "assistant" ? "MedMind" : "You"}
                  {msg.layer ? <span className="chip">Layer {msg.layer}</span> : null}
                  {msg.warning ? <span className="chip danger">Alert</span> : null}
                </div>
                <div className="chat-content">{msg.content}</div>
                {msg.report && msg.report.physical_summary?.length ? (
                  <div className="chat-report">
                    <div className="chat-report-title">Recent symptoms</div>
                    <ul>
                      {msg.report.physical_summary.map((p, i) => (
                        <li key={`${p.time}-${i}`}>
                          <span className="muted">{p.time}</span> — <span>{p.symptom}</span>
                          {p.severity ? <span className="chip soft">{p.severity}</span> : null}
                        </li>
                      ))}
                    </ul>
                    {msg.report.mental_note ? <div className="muted">Tâm trạng: {msg.report.mental_note}</div> : null}
                  </div>
                ) : null}
              </div>
            ))}
            {loadingMode && (
              <div className="chat-bubble assistant typing">
                <div className="chat-meta">MedMind</div>
                <div className="typing-dots">
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            )}
          </div>

          <div className="chat-input-row">
            <textarea
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onKeyDown={onKeyDown}
              placeholder="Type a question (e.g., patient summary or clinical suggestion)..."
              rows={2}
              disabled={!!loadingMode}
            />
            <button className="primary-btn" onClick={onSubmit} disabled={!!loadingMode}>
              {loadingMode ? "Sending..." : "Send"}
            </button>
          </div>
        </div>
      )}
    </>
  );
}
