import type {
  DoctorOverview,
  DoctorPatientList,
  EdgeMessage,
  EdgeMessageList,
  AIChatResponse,
  AIChatMode,
  PatientDashboard,
  PatientMedicationPlan,
  PatientTimeline,
  TimelineHorizon
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function fetchJSON<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    cache: "no-store",
    ...options
  });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json();
}

export async function getDoctorOverview(): Promise<DoctorOverview> {
  return fetchJSON<DoctorOverview>("/doctor/overview");
}

export async function getDoctorPatients(): Promise<DoctorPatientList> {
  return fetchJSON<DoctorPatientList>("/doctor/patients");
}

export async function getPatientTimeline(patientId: string, horizon: TimelineHorizon = "day"): Promise<PatientTimeline> {
  const search = new URLSearchParams({ horizon }).toString();
  return fetchJSON<PatientTimeline>(`/doctor/patients/${patientId}/timeline?${search}`);
}

export async function getPatientMedicationPlan(patientId: string): Promise<PatientMedicationPlan> {
  return fetchJSON<PatientMedicationPlan>(`/doctor/patients/${patientId}/medication_plan`);
}

export async function getPatientDashboard(patientId: string, horizon: "week" | "month" = "week"): Promise<PatientDashboard> {
  const search = new URLSearchParams({ horizon }).toString();
  return fetchJSON<PatientDashboard>(`/doctor/patients/${patientId}/dashboard?${search}`);
}

export async function listEdgeMessages(patientId?: string): Promise<EdgeMessageList> {
  const search = patientId ? `?${new URLSearchParams({ patient_id: patientId }).toString()}` : "";
  return fetchJSON<EdgeMessageList>(`/doctor/symptom_analytics/messages${search}`);
}

export async function createEdgeMessage(payload: {
  patient_id?: string;
  device_id?: string;
  speaker?: string;
  direction: "IN" | "OUT";
  content: string;
}): Promise<EdgeMessage> {
  return fetchJSON<EdgeMessage>(`/doctor/symptom_analytics/messages`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function clearEdgeMessages(patientId?: string): Promise<{ deleted: number }> {
  const search = patientId ? `?${new URLSearchParams({ patient_id: patientId }).toString()}` : "";
  return fetchJSON<{ deleted: number }>(`/doctor/symptom_analytics/messages${search}`, { method: "DELETE" });
}

export async function sendAIChat(payload: {
  question: string;
  mode: AIChatMode;
  patient_id?: string;
}): Promise<AIChatResponse> {
  return fetchJSON<AIChatResponse>("/ai/chat", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}
