"""
SQLAlchemy models namespace.

Models are organized by domain:
- User & profiles
- Devices & events
- Medication plans & dose occurrences
- Conversations & AI pipeline logs
- Notifications
- Analytics & embeddings
"""

from .user import User, UserRole
from .patient import Patient
from .caregiver import Caregiver
from .doctor import Doctor
from .patient_caregiver import PatientCaregiver
from .patient_doctor import PatientDoctor

from .device import Device
from .device_heartbeat import DeviceHeartbeat
from .device_event import DeviceEvent

from .medication import Medication
from .medication_plan import MedicationPlan
from .medication_plan_item import MedicationPlanItem
from .dose_occurrence import DoseOccurrence
from .dose_event_log import DoseEventLog

from .conversation import Conversation
from .interaction_log import InteractionLog
from .llm_request import LLMRequest
from .symptom_log import SymptomLog
from .medication_question_log import MedicationQuestionLog
from .alert_log import AlertLog
from .patient_profile import PatientProfile

from .notification_channel import NotificationChannel
from .notification_event import NotificationEvent
from .notification_delivery import NotificationDelivery

from .daily_patient_summary import DailyPatientSummary
from .weekly_patient_summary import WeeklyPatientSummary
from .health_insight import HealthInsight
from .health_report import HealthReport
from .embedding import Embedding
from .edge_text_log import EdgeTextLog
