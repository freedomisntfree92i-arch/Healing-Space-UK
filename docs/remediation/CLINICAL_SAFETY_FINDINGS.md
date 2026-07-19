# Clinical Safety Findings — Healing Space UK

_Initial engineering-side observations (2026-07-19). This is **not** a Clinical Safety Case and
carries no clinical sign-off — a qualified Clinical Safety Officer must own DCB0129 work
(EXTERNAL_ASSURANCE_REQUIRED). Findings are expanded in Phases §11–§14._

## CS-001 — Crisis escalation relies on email as primary channel (HIGH)
`safety_monitor.py` + risk routes dispatch alerts primarily by email; Twilio/webhook exist but must
be confirmed as reliable, retried, acknowledged. Spec §11.4: email must not be the sole acute-risk
channel. No durable escalation state machine or acknowledgement timers found (§11.3). No dead-letter.

## CS-002 — "Alerts within 1 minute" claimed without a staffed, tested service (HIGH)
`README.md:166`. No evidence of duty-rota staffing, delivery tracking, or acknowledgement SLA.
Remove the numeric claim (see CLAIMS_REGISTER); build service-availability config (§11.5).

## CS-003 — Risk may be reducible to a single score / AI judgement (HIGH)
`c_ssrs_assessment.py`, risk tables, and Groq risk context exist. Need to verify the LLM is not the
sole crisis detector (§15.4) and that risk events are immutable + auditable (§11.2). `risk_alerts`,
`risk_assessments`, `predictive_risk_flags` tables suggest scoring; confirm layered deterministic
rules precede/override the model.

## CS-004 — Safety plans may be overwritable (MEDIUM→HIGH)
Tables `safety_plans` + `enhanced_safety_plans` (two implementations — dedupe). Must confirm no
silent clinician overwrite, versioning, review dates, printable offline copy (§12).

## CS-005 — Safeguarding records not confirmed append-only (HIGH)
`safeguarding_concerns` table exists. Spec §13 requires immutable original + amendments (not
destructive edits), separate safeguarding permissions, statutory-deadline fields. Verify/implement.

## CS-006 — Under-18 / CYP pathway (MEDIUM)
No governed child/young-person pathway confirmed. Spec §13: enforce adult-only registration and
remove child-use claims unless a full CYP pathway exists.

## CS-007 — Assessment instruments need a controlled registry + golden-vector tests (HIGH)
Instruments present/implied: C-SSRS, PHQ-9, GAD-7 (README), plus `clinical_scales` table. No
assessment registry (name/version/licence/scoring/missing-answer rules) and scoring tests are not
verified against golden vectors (§14, §26.3). Licensing/permitted-use for each instrument unconfirmed.

## CS-008 — Patient-facing "screening ≠ diagnosis" framing (MEDIUM)
Confirm every assessment result screen states screening-not-diagnosis, item-level risk caveat, and
when clinical review is needed (§14). Crisis signposting in UI is present and correct (keep).
