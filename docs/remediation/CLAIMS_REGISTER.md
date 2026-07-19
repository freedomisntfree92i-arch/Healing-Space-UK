# Claims Register — Healing Space UK

_Every compliance/clinical/security claim found across README, UI templates, JS, policy text and
marketing material, classified per spec §2.3. **123 high-risk claim hits** were found (excluding
`_archive/`, `legacy/`, `backups/`). Classifications: PROVEN / PARTIAL / ASPIRATIONAL / FALSE /
NEEDS-INDEPENDENT-VERIFICATION / PROHIBITED-UNTIL-APPROVAL._

**Overriding rule:** no claim of NHS approval, clinical validation, trial/ethics approval, GDPR
compliance, medical-device status or specific encryption control may remain public without exact
evidence. Corrections are applied in Phase §2.3 (immediate) and re-verified per phase.

## The core contradiction (must resolve)

Public marketing asserts approvals that the **internal** dev notes explicitly deny:
- Public `README.md:20`: "**APPROVED FOR TRIALS** — Ethics approval obtained, clinical safety case
  validated." / `README.md:342`: "**Clinically Validated**".
- Internal `generate_dev_readme.py:519-521`: "Not FDA Approved… wellness tool only", "**No Clinical
  Validation: AI responses not clinically validated**", "Not HIPAA Certified".
- **The internal note is the truthful one.** All public approval/validation claims must be removed.

## PROHIBITED UNTIL APPROVAL (remove/rewrite immediately — fabricated or unverifiable approvals)

| Location | Claim | Action |
|---|---|---|
| `README.md:20` | "APPROVED FOR TRIALS – Ethics approval obtained, clinical safety case validated" | **Delete.** No evidence exists. Replace with "in development; not yet reviewed". |
| `README.md:342` | "Clinically Validated – C-SSRS, PHQ-9, GAD-7 implemented" | Reword: "implements C-SSRS/PHQ-9/GAD-7 scoring; **not independently validated**". |
| `README.md:274` | "3.3 Ethics Approval" | Remove implication of held approval; mark as required-future step. |
| `templates/landing.html:1550,1578,1987` | "NHS-Aligned · GDPR Compliant" trust badges | Remove/soften to "designed to align with…; pending independent review". |
| `templates/landing.html:1857` | "24/7 … clinician-supervised" | Remove "24/7" + "supervised" unless a staffed service is evidenced (§11.5). |

## FALSE / UNSUPPORTED (contradicted by implementation)

| Location | Claim | Reality |
|---|---|---|
| `README.md:157`, `README.md:242` | "AES-256 encryption at rest" | Encryption boundary unproven; spec §17 forbids this claim without evidence. Verify actual control, else remove. |
| `README.md:166` | "Clinician alerts within 1 minute" | No staffed, tested SLA; email is primary channel. Remove numeric SLA (§11.3). |
| `OUTREACH_EMAILS_PRIORITY_TARGETS.md:188` | "Fully GDPR compliant… Encryption end-to-end" | No E2E encryption; not certified. Rewrite. |
| `safety_monitor.py:11` | "Fully GDPR compliant (no storage of messages)" | Overstated; verify + soften. |
| `TIKTOK_SCRIPTS_VIRAL.md:42`, `VIDEO_SCRIPTS_WORLD_CLASS.md:264,340` | "AI therapy that works 24/7 / your own AI therapist" | Positions AI as autonomous therapy; §15.1 forbids. Reword to "supportive, non-diagnostic". |

## NEEDS INDEPENDENT VERIFICATION (may be true but require external evidence)

| Location | Claim |
|---|---|
| `templates/landing.html:1550,1940` | "WCAG 2.1 AA", "Encrypted in transit (TLS 1.3) & at rest, UK GDPR compliant" — needs external a11y audit (§20) + evidenced TLS/at-rest config (§17). |
| `README.md:103,143`; `static/js/activity-logger.js:7` | "GDPR-compliant data management" — needs DPIA + lawful-basis register (§16) before any compliance claim. |
| `BUSINESS_DEVELOPMENT_GUIDE.md:16,657` | "GDPR/HIPAA-ready infrastructure" — "ready" is softer but still needs evidence. |

## ASPIRATIONAL (acceptable if clearly framed as future/in-progress)

- "Designed to support NHS deployment", roadmap language — retain only with "in development /
  pending independent review / not an emergency service" framing.

## PARTIAL / PROVEN (keep, with accurate wording)

- Crisis signposting in UI (`landing.html:1485`, `c_ssrs_assessment.py:257`, `clinician.js:1586`):
  Samaritans 116 123, 999, SHOUT 85258 — **factually correct and valuable; keep.**
- "CSRF tokens, rate limiting" (`README.md:242`): mechanisms exist but are weak (SEC-001/004) —
  do not present as robust until fixed.

## Required replacement phrasing (spec §2.3)
"designed to support", "implementation in progress", "pending independent review", "not an
emergency service", "availability depends on the participating service", "screening result, not a
diagnosis", "not independently validated".

## Full evidence
123 raw hits captured via repo-wide grep; the table above lists the material offenders. Re-run:
`grep -rniaE "NHS[ -](approved|compliant|ready)|clinically validated|GDPR[ -]?compliant|AES-?256|ethics approv|24/7|one[ -]minute" --include=*.md --include=*.html --include=*.py --include=*.js .`
