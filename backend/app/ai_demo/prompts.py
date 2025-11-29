# prompts.py

# --- LAYER 1 PROMPTS ---
LAYER_1_SYSTEM_ROLE = "You are a professional medical scribe."

LAYER_1_USER_PROMPT = """
Task: Summarize the patient's daily health logs into a structured report.

Input Logs:
{logs}

Requirements:
1. 'physical_summary': List of objects with 'time' and 'symptom'.
2. 'mental_note': Extract mental health info.
3. 'warning_flag': Boolean (true/false).
4. 'narrative': A professional paragraph summarizing the daily health status for a doctor to read quickly.

OUTPUT FORMAT: Return ONLY a raw JSON object containing these 4 fields.
"""

# --- LAYER 2 PROMPTS ---
# (Giữ nguyên như cũ, không đổi)
LAYER_2_SYSTEM_ROLE = "You are a helpful cardiac specialist assistant."

LAYER_2_USER_PROMPT = """
Task: Analyze the daily report against the patient's medication records and provide advice.

Data Source 1 (Daily Report):
{report}

Data Source 2 (Medical Records):
{records}

Logic:
- Compare daily symptoms with medication side effects.
- If symptoms match known side effects (e.g., dizziness from Nitroglycerin), reassure the patient.
- If symptoms are severe or unrelated to meds, suggest seeing a doctor.
- Ignore 'mental_note' unless it is critical.

OUTPUT FORMAT: Provide a clear, direct suggestion paragraph addressed to the patient (use 'You'). Do not include headers or bullet points.
"""