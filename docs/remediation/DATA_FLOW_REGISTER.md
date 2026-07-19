# Data Flow Register — Healing Space UK

_Initial data flows identified from code (2026-07-19). Expanded into `docs/architecture/DATA_FLOWS.md`
with diagrams in Phase §28. Data classes per spec §16.1: SC = special-category health data,
P = personal, SEC = security-sensitive, SG = safeguarding-restricted._

| # | Flow | Data class | Destination | Notes / risk |
|---|---|---|---|---|
| DF-1 | Patient → therapy chat → **Groq LLM** → response stored (`chat_history`, `ai_memory*`) | SC | External (Groq) | Off-platform SC data; needs DPA + retention (PRIV-002/003) |
| DF-2 | Patient → assessments (PHQ-9/GAD-7/C-SSRS) → `*_assessments`, `clinical_scales` | SC | Internal DB | Scoring must be tested (§14/§26.3) |
| DF-3 | Risk signal → `risk_alerts`/`risk_assessments`/`predictive_risk_flags` → **email/SMS/webhook** alert | SC/SG | Internal + Twilio/SMTP/webhook | Escalation not durable (CS-001); channels external |
| DF-4 | Patient ↔ clinician **messaging** → `messages`, `message_receipts`, `conversations` | SC/P | Internal DB | CSRF-exempt endpoints (SEC-001); delivery semantics §18 |
| DF-5 | Safeguarding disclosure → `safeguarding_concerns` | SG | Internal DB | Must be append-only (CS-005) |
| DF-6 | Safety plan → `safety_plans`/`enhanced_safety_plans` | SC | Internal DB | Versioning/overwrite risk (CS-004) |
| DF-7 | **Training export** → `export_training_data.py` → files (cron) | SC→pseudonymised | Local files / external? | Ungoverned (PRIV-001); disable by default |
| DF-8 | Exports: FHIR/CSV/PDF/professional-summary | SC/P | Download | CSV formula-injection + authz + encryption needed (§22) |
| DF-9 | Auth: registration/login/reset → `users`, `verification_codes`, email links | P/SEC | Internal + SMTP | Reset-token security (§6.4); no clinical content in email (§16.7) |
| DF-10 | TTS: text → **edge-tts (Microsoft)** → `speech.mp3` | P/SC? | External (Microsoft) | Off-platform text transmission (PRIV-003) |
| DF-11 | Audit: actions → `audit_logs` via `log_event` | SEC | Internal DB/logs | Must not log SC content (PRIV-004) |
| DF-12 | Consent: `data_consent`, `ai_monitoring_consent` | P | Internal DB | Must actually gate DF-1/DF-7 (PRIV-002) |

## Highest-risk flows
DF-1, DF-7, DF-10 (external transmission of sensitive text) and DF-3 (crisis escalation reliability)
are the priority for privacy + clinical-safety remediation.
