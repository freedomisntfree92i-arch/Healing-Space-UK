# Privacy & Data-Protection Findings — Healing Space UK

_Engineering observations (2026-07-19). A DPIA and lawful-basis register (Phase §16, §28) require
Information Governance ownership — see EXTERNAL_ASSURANCE_REQUIRED. No "GDPR compliant" claim is
supportable yet (see CLAIMS_REGISTER)._

## PRIV-001 — AI training-data export pipeline is active and not governed (CRITICAL)
`export_training_data.py`, `training_data_manager.py` ("GDPR-compliant training data"),
`setup_training_export_cron.sh`, route `/api/training/export`. Spec §15.7 requires training exports
**disabled by default** until a governance workflow exists (approval, pseudonymisation, free-text
de-identification, disclosure-risk assessment, manifest, withdrawal). "Hashing usernames is not
anonymisation." **Action (Phase §15.7):** disable by default behind a governance flag.

## PRIV-002 — Clinical data can flow into AI without purpose-limitation controls (HIGH)
Groq receives patient message text and risk context. No engineering control found preventing
clinical data flowing to training/analytics/debug (§16.3). `ai_monitoring_consent` +
`data_consent` tables exist — verify they actually gate processing.

## PRIV-003 — Off-platform transmission of sensitive text (HIGH)
Groq (LLM) and edge-tts (Microsoft TTS) both transmit potentially health-related text externally.
Must appear in DPIA + subprocessor register with region/retention (§16, THIRD_PARTY_REGISTER).

## PRIV-004 — Logging may include sensitive content (HIGH — verify)
`log_event(...)` is used widely (incl. security events with endpoint/IP). Must verify no full
messages, assessment answers, safety-plan/safeguarding text, tokens, secrets or reset links reach
logs (§16.7). Implement structured identifiers + redaction.

## PRIV-005 — No retention jobs / DSAR workflow (HIGH)
No controlled retention scheduler or data-subject-request workflow found (§16.5/§16.6). Deletion
appears manual (destructive scripts). Must not allow unlawful deletion of clinically/safeguarding-
required records.

## PRIV-006 — Encryption boundary undocumented (HIGH)
"AES-256 at rest" claimed (README) but the actual boundary (DB/storage vs app-field vs transport vs
backups) is undocumented (§17). Confirm real controls; correct the claim.

## PRIV-007 — Patient transparency view absent (MEDIUM)
No patient-facing data-access dashboard (what data exists, who accessed, which AI processed,
consent state) — §16.4. Build after foundations.

## PRIV-008 — Anonymisation salt handling (MEDIUM)
`ANONYMIZATION_SALT` used for pseudonymisation; verify it is not a single static repo/env value that
enables re-identification, and that free-text is de-identified for any research/training export.
