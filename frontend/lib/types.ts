export type DoseEventStatus = "ON_TIME" | "LATE" | "MISSED";
export type TimelineHorizon = "day" | "hour";

export type DoseEvent = {
  id: string;
  label: string;
  status: DoseEventStatus;
  time: string;
};

export type DoctorOverview = {
  metrics: {
    patients: number;
    adherence_rate: number;
    emergency_signals_week: number;
    ai_insights: number;
  };
  adherence_trend: { label: string; value: number }[];
  symptom_frequency: { label: string; value: number }[];
  alerts: { message: string; level: string; time?: string }[];
  adherence_summary: {
    mean: number;
    high_count: number;
    medium_count: number;
    low_count: number;
  };
  on_time_summary: {
    mean: number;
    high_count: number;
    medium_count: number;
    low_count: number;
  };
  missed_summary: {
    total_7d: number;
    total_30d: number;
    per_patient_week: number;
    top_patients: { patient_id: string; patient_name: string; missed_7d: number }[];
  };
  symptom_population: {
    total_7d: number;
    total_30d: number;
    top: { symptom: string; count: number }[];
  };
  severity_population: {
    change_pct: number;
    direction: string;
    patients_up: number;
    flagged_patients: number;
  };
  new_symptoms_population: {
    events: number;
    patient_count: number;
    top: { symptom: string; count: number }[];
    critical_patients: number;
  };
  symptom_by_patient: {
    labels: string[];
    series: { label: string; values: number[] }[];
  };
  ai_notifications: { patient_id: string; patient_name: string; summary: string; detail: string }[];
};

export type DoctorPatient = {
  id: string;
  name: string;
  adherence: number;
  alerts: number;
  last_update?: string;
};

export type DoctorPatientList = {
  patients: DoctorPatient[];
};

export type PatientTimeline = {
  patient_id: string;
  points: { label: string; adherence: number; alerts: number }[];
};

export type PatientProfileCard = {
  id: string;
  name: string;
  age?: number | null;
  gender?: string | null;
  avatar_url?: string | null;
  medical_history: string[];
  current_medications: string[];
  allergies: string[];
  primary_complaint?: string | null;
  lifestyle_factors: string[];
  recent_tests: string[];
  treatment_plan: string[];
};

export type DashboardHorizon = "week" | "month";

export type AdherenceKPIs = {
  horizon: DashboardHorizon;
  overall_adherence_rate: number;
  on_time_rate: number;
  missed_doses: number;
};

export type SymptomTrending = {
  symptom: string;
  count: number;
};

export type SeverityTrend = {
  change_pct: number;
  direction: "up" | "down" | "flat";
};

export type SeverityBar = {
  label: string;
  normal: number;
  warning: number;
  alert: number;
};

export type NewSymptom = {
  symptom: string;
  first_seen: string;
};

export type SymptomKPIs = {
  horizon: DashboardHorizon;
  frequency: number;
  trending: SymptomTrending[];
  severity_trend: SeverityTrend;
  severity_bars: SeverityBar[];
  new_symptoms: NewSymptom[];
};

export type EdgeMessage = {
  id: string;
  patient_id: string;
  patient_name: string;
  device_id?: string | null;
  speaker?: string | null;
  direction: "IN" | "OUT";
  content: string;
  intent?: string | null;
  created_at: string;
};

export type EdgeMessageList = {
  patient_id: string;
  patient_name: string;
  messages: EdgeMessage[];
};

export type PatientDashboard = {
  patient: PatientProfileCard;
  adherence: AdherenceKPIs;
  symptoms: SymptomKPIs;
};

export type PatientMedicationPlan = {
  patient_id: string;
  patient_name: string;
  doses: {
    med_name: string;
    dose: string;
    time: string;
    status: string;
    symptom?: string | null;
  }[];
};

export type AIChatMode = "summary" | "suggestion";

export type AIChatReport = {
  physical_summary?: { time: string; symptom: string; severity?: string | null }[];
  mental_note?: string | null;
  warning_flag?: boolean | null;
};

export type AIChatResponse = {
  patient_id: string;
  patient_name: string;
  mode: AIChatMode;
  layer: number;
  message: string;
  narrative?: string | null;
  warning_flag?: boolean | null;
  report?: AIChatReport | null;
};
