# Privacy & Data-Protection Findings — Healing Space UK

_Engineering observations (2026-07-19). A DPIA and lawful-basis register (Phase §16, §28) require
Information Governance ownership — see EXTERNAL_ASSURANCE_REQUIRED. No "GDPR compliant" claim is
supportable yet (see CLAIMS_REGISTER)._

## PRIV-001 — AI training-data export pipeline is active and not governed — ✅ DISABLED BY DEFAULT (2026-07-19)
**Status:** contained. Added `TRAINING_DATA_ENABLED` flag (default **off**) gating BOTH live paths:
(1) `/api/training/export` now returns 403 `TRAINING_EXPORT_DISABLED` unless explicitly enabled;
(2) the auto-collection of therapy sessions into the training corpus during normal chat
(`api.py` ~line 9743) now requires the flag too, so clinical chat no longer auto-flows into training.
`setup_training_export_cron.sh` refuses to install unless the flag is set. (`export_training_data.py`
was already a hard-disabled deprecated stub.) Tests: `tests/backend/test_training_export_disabled.py`.
**Still REQUIRED before enabling (full §15.7 governed workflow):** authenticated/authorised requester
(the endpoint currently trusts a `username` in the body — an authz hole to close), approved purpose,
pseudonymisation, free-text de-identification, disclosure-risk assessment, cohort threshold, immutable
manifest, withdrawal handling. "Hashing usernames is not anonymisation."

## PRIV-002 — Clinical data can flow into AI without purpose-limitation controls (HIGH)
Groq receives patient message text and risk context. No engineering control found preventing
clinical data flowing to training/analytics/debug (§16.3). `ai_monitoring_consent` +
`data_consent` tables exist — verify they actually gate processing.

## PRIV-003 — Off-platform transmission of sensitive text (HIGH)
Groq (LLM) and edge-tts (Microsoft TTS) both transmit potentially health-related text externally.
Must appear in DPIA + subprocessor register with region/retention (§16, THIRD_PARTY_REGISTER).

## PRIV-004 — Logging may include sensitive content — 🟡 MOSTLY VERIFIED + leaks fixed (2026-07-19)
**Findings after audit:** `log_event()` writes to the **`audit_logs` DB table** (controlled record),
not stdout, and logs metadata not content — acceptable. The 185 call sites sampled log event
types/IDs (e.g. "Chat message sent"), not message bodies. **Fixed real stdout leaks (§16.7):**
- Groq content-filter / API error handlers logged `response.text[:300]`, which can echo the user's
  flagged message content (api.py ~3285/3298 and dev-AI ~8352) → now log status + length only.
- `send_message` logged the message **subject** (`subject[:50]`) → now logs `subject_len` only.
**Still open / tracked:** systematic log-redaction test harness (§26); `audit.py` connects only via
`DATABASE_URL` (silently no-ops under `DB_*`-only local dev) and opens a NEW connection per call
(not pooled — §5.3 connection budget). No dedicated automated test added for the redactions (string
changes verified by inspection + no-regression suite).

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
