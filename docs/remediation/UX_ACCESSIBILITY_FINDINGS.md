# UX & Accessibility Findings — Healing Space UK

_Preliminary observations (2026-07-19). Full audit is Phase §19–§20. Automated checks cannot prove
accessibility; independent testing is required before any WCAG conformance claim
(EXTERNAL_ASSURANCE_REQUIRED). "WCAG 2.1 AA" currently claimed in `landing.html` is unverified._

## UX-001 — Frontend is large monolithic templates + root-level 160 KB `appUpdates.js` (HIGH)
Patient UI concentrated in big templates/JS with inline handlers. Spec §19 requires splitting into
layouts/components/pages/api/state/accessibility modules; remove duplicate IDs, inline handlers,
global functions. Inline JS/CSS also blocks a strict CSP (SEC-009 / §9).

## UX-002 — Information architecture not aligned to spec (MEDIUM)
Confirm/implement patient IA (Today/Talk/My plan/Tools/Progress/Messages/Appointments/Safety/
Profile) and clinician IA (Caseload/Risk inbox/…). First screen should prioritise wellbeing +
urgent support + next action, not present every tool at once (§19.1–19.2).

## UX-003 — Persistent crisis access (MEDIUM, partially present)
Crisis signposting exists on the landing page and some JS (Samaritans/999/SHOUT — correct). Must be
a **persistent** entry on every patient page, not dependent on AI chat (§11.6/§19.3).

## UX-004 — Gamification safety (MEDIUM)
Tables `achievements`, `spell_mastery`, `quest_*`, `pet*` indicate gamification. Spec §19.5 prohibits
broken-streak shame, competitive ranking, rewards for crisis disclosure, celebratory animation after
severe-risk results; require opt-out + gentle "welcome back" language. Audit for these.

## UX-005 — Failure states & clinical language (MEDIUM)
Define explicit offline/reconnecting/failed-save/queued/AI-unavailable states (§19.7). Replace formal
instrument names in primary navigation with patient-friendly labels (§19.6).

## UX-006 — Accessibility baseline unverified (HIGH)
No automated a11y test harness found. Implement + verify keyboard nav, focus, semantic headings,
labels, non-colour risk indicators, reduced motion, 400% zoom/reflow, accessible charts, printable
accessible safety plan (§20). Add automated checks (axe) — but do not claim certification.
