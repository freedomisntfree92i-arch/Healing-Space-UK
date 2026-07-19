# Implementation Status — Healing Space UK Remediation

> **READ THIS FIRST each session.** It is the single source of continuity so work resumes without
> re-running the whole audit (spec §31).

## Snapshot
- **Branch**: `security/nhs-grade-remediation` (off `main`)
- **Latest commit**: _(Phase 0 deliverables not yet committed — pending user approval)_
- **Current phase**: Phase 0 (Baseline & deliverables) — **complete, awaiting approval to start Phase Zero §3**
- **Last updated**: 2026-07-19

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

## Exact next task (Phase Zero — §3, on approval)
1. Repo hygiene: fix `.gitignore`/`.gitattributes`; `git rm --cached` the tracked junk
   (`node_modules/`, `__pycache__`/`.pyc`, `cookies.txt`, `flask.pid`, `speech.mp3`, `backups/`,
   `.~lock*`, `_archive/*.deb`/`*.apk`). Preserve files on disk; only untrack.
2. Add `.github/CODEOWNERS`, `dependabot.yml`, `SECURITY.md`;
   `docs/security/SECRET_ROTATION_RUNBOOK.md`, `REPOSITORY_EXPOSURE_RESPONSE.md`.
3. Verify git history for secrets (git log -p over sensitive paths / trufflehog-style scan);
   produce the exact rotation checklist. **Do not rewrite history yet** — report findings first.
4. **Neutralise destructive endpoints** SEC-002: `/api/admin/wipe`, `/api/admin/wipe-database`,
   `/api/admin/reset-users`, `/api/debug/*` → remove routes; relocate any real need to an offline
   CLI guarded by env + confirmation. Add tests asserting the routes return 404/gone.
5. Re-run the baseline suite; confirm no regression vs 805 passing.

## Known critical/high items being tracked
SEC-001 (broken CSRF), SEC-002 (HTTP DB wipe), SEC-003 (developer superuser), SEC-004 (in-memory
rate limit), SEC-005 (history secrets), PRIV-001 (ungoverned training export), CS-001/003
(crisis escalation + single-score risk), plus the fabricated approval/validation claims (§2.3).

## Continuity rule
When context runs low: update this file (completed / branch / latest commit / test status /
unresolved risks / exact next task), commit, and resume from here next session.
