# Implementation Status — Healing Space UK Remediation

> **READ THIS FIRST each session.** It is the single source of continuity so work resumes without
> re-running the whole audit (spec §31).

## Snapshot
- **Branch**: `security/nhs-grade-remediation` (off `main`)
- **Latest commit**: SEC-001 CSRF fix (Phase Zero = `c08e727`; Phase 0 = `d6eafa9`)
- **Current phase**: **Foundations — SEC-001 (CSRF §8) COMPLETE. Awaiting approval for next.**
- **Last updated**: 2026-07-19

## SEC-001 CSRF fix (§8) — done 2026-07-19
- Session-bound, constant-time CSRF validation; stable per-session token; removed the
  "any 64-char alnum passes" bypass; startup guard refuses TESTING in prod/non-DEBUG.
- Fixed `clinician.js` token field; `/api/csrf-token` returns `csrf_token`+`token`.
- Tests: `tests/backend/test_csrf_protection.py` (7) + updated `test_auth.py::TestCSRFToken`.
  **818 passed / 129 failed / 71 errors / 17 skipped** — no regression (+8 new).
- Deferred to §8 consolidation: the 2nd class-based CSRF system + CSRF-exempt messaging endpoints.

## 🔴 URGENT USER ACTION OUTSTANDING
A real Railway Postgres password was found in git history (`zkzFIlnbBIFNTomTawKPymiZwhWpvYfG`).
**Rotate it in Railway now** (see `docs/security/SECRET_ROTATION_RUNBOOK.md`). History purge is
planned but the credential stays valid until rotated. Not fixable by code.

## Phase Zero results (§3) — done 2026-07-19
- Removed 4 destructive HTTP routes from `api.py` (`/api/admin/wipe`, `/api/admin/wipe-database`,
  `/api/admin/reset-users`, `/api/debug/analytics/<clinician>`); replaced DB-wipe/reset capability
  with offline `scripts/admin_cli.py` (prod-refusing, typed confirmation). SEC-002 closed.
- Untracked 1099 junk files (node_modules, __pycache__/pyc, backups/, cookies.txt, flask.pid,
  speech.mp3, locks, apk/deb) — kept on disk; extended `.gitignore`; added `.gitattributes`.
- Added `.github/CODEOWNERS`, `dependabot.yml`, `SECURITY.md`; `docs/security/SECRET_ROTATION_RUNBOOK.md`
  + `REPOSITORY_EXPOSURE_RESPONSE.md`.
- Verified git history for secrets (SEC-005 confirmed — see URGENT above). **No history rewrite done.**
- Added `tests/backend/test_destructive_routes_removed.py` (regression guard).
- Tests: **810 passed / 129 failed / 71 errors / 17 skipped** — no regression vs 805 baseline (+5 new).

## Test baseline (do not regress below this)
- Env: isolated venv at `scratchpad/venv` (runtime + pytest); local Postgres 16 present but the
  test DB `healing_space_test` is not authenticated for the conftest credentials.
- Command: `python -m pytest tests/ -o addopts="" --timeout=120 -q`
- Result: **805 passed, 129 failed, 71 errors, 17 skipped** (27s).
- Red is dominated by **test-harness gaps**, not proven product regressions:
  - ~71 errors = missing conftest fixtures (`test_db_connection`, `clinician_user`, `auth_session`,
    `patient_user`, `authenticated_session`).
  - ~57 = `401` cascading from those missing auth fixtures.
  - ~18 = Postgres auth failure (conftest password mismatch) + a few `500`s to investigate.
- The 805 passing are the mock-based unit tests. Fixing the harness is part of §26.

## Completed
- ✅ Grounding survey of repo (read-only).
- ✅ Branch created.
- ✅ Baseline test run recorded (above).
- ✅ `docs/remediation/*` deliverables authored (12 files).
- ✅ `scripts/gen_route_matrix.py` added (regenerates the route matrix from `api.py`).

## Open decisions (from user)
- Sequencing = **phase-by-phase, approve each**.
- Git history = **verify + document first, then targeted purge** (safe: solo repo). Credential
  rotation is a **user action** (Railway/Gmail/Groq/Twilio) — never mark done by code.
- Fork/remote note: local remote is `shadowWolf88/Healing-Space-UK`; spec header named
  `freedomisntfree92i-arch`. Confirm canonical remote before any push.

## Exact next task (Foundations, on approval — recommend starting §4 architecture or §8 CSRF)
Recommended first Foundations target: **SEC-001 (broken CSRF, §8)** — highest-severity live code
issue now that SEC-002 is closed. Alternatively begin the §4 modular split of `api.py`. Also early:
**PRIV-001** disable AI-training export by default (§15.7). Confirm sequencing with user.

## Known critical/high items being tracked
SEC-001 (broken CSRF), SEC-002 (HTTP DB wipe), SEC-003 (developer superuser), SEC-004 (in-memory
rate limit), SEC-005 (history secrets), PRIV-001 (ungoverned training export), CS-001/003
(crisis escalation + single-score risk), plus the fabricated approval/validation claims (§2.3).

## Continuity rule
When context runs low: update this file (completed / branch / latest commit / test status /
unresolved risks / exact next task), commit, and resume from here next session.
