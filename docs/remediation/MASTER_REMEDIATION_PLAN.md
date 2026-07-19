# Master Remediation Plan — Healing Space UK

_Branch: `security/nhs-grade-remediation`. Started 2026-07-19. Working method: **phase-by-phase with
approval gates** — one phase, then a §30-format status report, then wait for approval. Overriding
constraint: **never break working behaviour** (capture a regression baseline before any schema/flow
change)._

## Goal
Make Healing Space UK technically robust, privacy-preserving and clinically responsible — capable of
*progressing toward* NHS assurance. Code cannot grant approval; where external review is required we
build the evidence and mark it honestly (see `EXTERNAL_ASSURANCE_REQUIRED.md`). No fabricated
approvals, dates, names, trials or test results.

## What this repo actually is (verified)
A 27,456-line / 380-route single-file Flask monolith (`api.py`) on raw psycopg2/PostgreSQL, with a
Capacitor mobile wrapper, an active Groq LLM integration, an ungoverned AI-training-export pipeline,
live HTTP database-wipe endpoints, effectively-decorative CSRF, in-memory rate limiting, schema
created at startup (no migrations), and public marketing claims contradicted by internal dev notes.

## Deliverables in this folder
| File | Status |
|---|---|
| `REPOSITORY_INVENTORY.md` | ✅ populated |
| `ROUTE_SECURITY_MATRIX.md` | ✅ generated (380 routes) via `scripts/gen_route_matrix.py` |
| `SECURITY_FINDINGS.md` | ✅ SEC-001..009 (verified) |
| `CLAIMS_REGISTER.md` | ✅ 123 hits classified |
| `CLINICAL_SAFETY_FINDINGS.md` | ✅ CS-001..008 |
| `PRIVACY_FINDINGS.md` | ✅ PRIV-001..008 |
| `UX_ACCESSIBILITY_FINDINGS.md` | ✅ UX-001..006 |
| `DATA_FLOW_REGISTER.md` | ✅ DF-1..12 |
| `THIRD_PARTY_REGISTER.md` | ✅ subprocessors listed |
| `EXTERNAL_ASSURANCE_REQUIRED.md` | ✅ EXT-1..12 |
| `IMPLEMENTATION_STATUS.md` | ✅ living continuity file — **read this first each session** |
| `MASTER_REMEDIATION_PLAN.md` | ✅ this file |

## Phase order (mapped to spec §§)
0. **Baseline & deliverables** (this) — ✅ done pending user approval.
1. **Phase Zero containment** (§3) — kill destructive endpoints, git hygiene, secret exposure
   verification + rotation checklist. **NEXT.**
2. Foundations — architecture (§4), migrations/DB (§5), auth (§6), authz (§7), CSRF/CORS/validation
   (§8), headers (§9), rate limiting (§10).
3. Clinical & safety (§11–§14).
4. AI & data protection (§15–§17).
5. Product surfaces (§18–§23).
6. DevSecOps / resilience / evidence (§24–§29).

## Top 5 risks to burn down first
1. SEC-002 HTTP DB-wipe endpoints (Phase Zero).
2. SEC-001 broken CSRF (§8).
3. PRIV-001 ungoverned AI-training export (§15.7) — disable-by-default early.
4. SEC-005 secrets in git history (Phase Zero, verify → purge).
5. Fabricated approval/validation claims (§2.3) — correct immediately.

## Definition of Done
The 37 items in spec §29, re-verified per phase; external items honestly flagged, never claimed.
