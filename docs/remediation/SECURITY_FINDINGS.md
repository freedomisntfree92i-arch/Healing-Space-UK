# Security Findings — Healing Space UK

_Derived from direct code inspection on 2026-07-19. Severity: CRITICAL / HIGH / MEDIUM / LOW.
Each finding notes the phase that fixes it. "Verified" = confirmed by reading the code; findings
without a fix committed yet are open. This is an internal engineering register, **not** a
penetration-test report — independent testing is still required (spec §26.5, EXTERNAL_ASSURANCE)._

## CRITICAL

### SEC-001 — CSRF protection is effectively decorative (not session-bound)
- **Where**: `api.py` `validate_csrf_token()` (~line 2379) + `csrf_protect()` before_request (2414).
- **Detail**: The global validator returns `True` for **any** 64-char alphanumeric string and is
  fully bypassed when `TESTING=1`. Tokens are never stored server-side or bound to the session; the
  code comment concedes "In production, you'd want to validate against stored session tokens."
  The `/api/csrf-token` cookie is not compared against the header (no real double-submit).
- **Impact**: All 212 state-changing routes are practically CSRF-forgeable. Also several sensitive
  endpoints (`send_message`, `get_inbox`, `mark_message_read`, `delete_message`) are in
  `CSRF_EXEMPT_ENDPOINTS`, "handled via session auth" — session auth does not stop CSRF.
- **Fix**: Phase §8.1 — adopt a vetted, session-bound CSRF mechanism; remove the TESTING blanket
  bypass; add negative tests (no/invalid/expired/foreign-session/replay/cross-origin).

### SEC-002 — Destructive database operations exposed over HTTP
- **Where**: `/api/admin/wipe` (6827), `/api/admin/wipe-database` POST (6967),
  `/api/admin/reset-users` POST (14749), `/api/debug/analytics/<clinician>` (6863); plus
  `reset_railway_db.py`. Gated only by env flags (`ADMIN_WIPE_KEY`, `ALLOW_ADMIN_RESET`).
- **Impact**: A web request can wipe the clinical database. Env-flag gating is not sufficient.
- **Fix**: Phase Zero §3.2 — remove the routes; move any legitimate need to an offline CLI command
  with explicit environment guard + human confirmation. No web path may reset the DB.

### SEC-003 — `developer` role acts as a clinical-data superuser
- **Where**: `developer_dashboard` (6842), `developer_ai_chat` (8346), `developer_register` (8116),
  `developer_stats`, and `dev_*` tables (`dev_ai_chats`, `dev_jobs`, `dev_messages`,
  `dev_terminal_logs`, `developer_test_runs`).
- **Impact**: A non-clinical role can reach clinical data/actions; violates spec §7.1
  ("Do not use a `developer` role as a clinical-data superuser").
- **Fix**: Phase §7 — central permission model; strip clinical reach from `developer`.

## HIGH

### SEC-004 — Rate limiting is in-memory (non-distributed) and duplicated
- **Where**: Flask-Limiter `storage_uri="memory://"` (321); a second custom in-memory
  `RateLimiter` (2566) behind `@check_rate_limit` on ~12 endpoints (global mutable state, §4.3).
- **Impact**: Limits reset on restart and are per-worker — ineffective across workers/replicas;
  brute-force/abuse protection is unreliable. Two parallel systems = inconsistent enforcement.
- **Fix**: Phase §10 — single distributed limiter (Redis, `NEEDS-INFRA`); per-endpoint limits.

### SEC-005 — Likely secrets in git history
- **Where**: presence of `remove_secrets.py`, `secrets_manager.py`, and a docs file
  `RAILWAY_SECRET_KEY_FIX.md` strongly implies credentials were committed historically.
- **Impact**: Exposed API keys / DB URLs / SMTP creds remain retrievable from history even if
  deleted from HEAD.
- **Fix**: Phase Zero §3.1 — verify history, produce exposure-response + rotation checklist, then
  targeted history purge (DECISION: verify first). **Rotation is a user action** — not claimed done.

### SEC-006 — 67 state-changing routes with no inline authentication detected
- **Where**: see ROUTE_SECURITY_MATRIX "no detectable authentication" table.
- **Impact**: Some are legitimately public (login/register/webhooks); others may be genuine
  authorization holes. Cannot be assured by inspection because auth is inline, not centralised.
- **Fix**: Phase §7 — centralise authN/authZ; manually confirm each of the 67 and close real gaps.

### SEC-007 — CSRF `TESTING=1` bypass + weak session model
- **Where**: `TESTING` env disables CSRF; 4-hour inactivity timeout only; `remember_me` sessions
  skip inactivity entirely (`check_session_inactivity`, 2438).
- **Impact**: No server-side session revocation, no absolute cap enforcement for "remember me",
  no rotation on privilege change.
- **Fix**: Phase §6.3 — session rotation/revocation, idle + absolute timeouts, device list.

## MEDIUM

### SEC-008 — Raw SQL throughout a 27k-line handler layer
- **Where**: `api.py` uses `psycopg2` string queries directly in route handlers (no repository
  layer). Parameterisation appears used in sampled handlers (good), but coverage is unverified
  across 380 routes; `SELECT *` and dynamic fragments need auditing (spec §5.2).
- **Fix**: Phase §4/§5 — repository layer, explicit columns, statement timeouts; SQLi tests §26.5.

### SEC-009 — CORS / content-type / headers need verification against strict policy
- **Where**: `flask-cors` CORS, `validate_content_type` before_request (2395), `after_request`
  header setter (2080) with a CSP referencing `cdn.jsdelivr.net` and inline usage.
- **Impact**: CSP likely relies on `unsafe-inline` (inline JS/CSS present); CORS allowlist must be
  confirmed to exclude wildcard-with-credentials.
- **Fix**: Phase §8.2 / §9 — strict CSP without unsafe-inline (refactor inline), CORS allowlist.

## Notes / positive findings (preserve)
- A startup guard already rejects short `SECRET_KEY` (<32 chars) — keep/extend for prod fail-closed.
- `verify_clinician_patient_relationship()` already exists — reuse as the basis for the single
  patient-access policy (§7.2) rather than reinventing.
- A `validate_content_type` before_request already enforces JSON — extend, don't replace.
- `cbt_tools/` is already a clean blueprint-style module — use it as the refactor template (§4).
