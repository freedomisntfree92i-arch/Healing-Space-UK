# Repository Inventory — Healing Space UK

_Derived from the actual repository on 2026-07-19 (branch `security/nhs-grade-remediation`).
The code is the source of truth; this inventory supersedes documentation claims._

## 1. Application shape

- **Backend**: single-file Flask monolith `api.py` — **27,456 lines / 1.16 MB, 380 routes**.
- **Framework/stack**: Flask 3.x, `flask-cors`, `flask-limiter`; **raw `psycopg2`** (connection
  pool) — **no ORM**; PostgreSQL runtime.
- **Templating**: Jinja templates in `templates/` (incl. large `landing.html`).
- **Frontend**: `static/js/*` (`clinician.js`, `activity-logger.js`, …), `static/css/*`;
  plus a 160 KB `appUpdates.js` at repo root.
- **Mobile**: Capacitor (`capacitor.config.json`) with `android/` (Java) and `ios/` (Swift)
  wrappers; duplicated older copies under `legacy/`.

## 2. Backend modules (Python, repo root unless noted)

| Module | Purpose |
|---|---|
| `api.py` | Monolith: all 380 routes, auth, CSRF, DB access, AI, exports |
| `ai_trainer.py`, `train_model.py`, `train_scheduler.py`, `training_config.py`, `training_data_manager.py`, `export_training_data.py` | **AI training-data pipeline** (see §7) |
| `c_ssrs_assessment.py`, `demo_c_ssrs.py` | C-SSRS risk assessment logic |
| `safety_monitor.py` | Crisis/keyword safety monitoring |
| `message_service.py`, `messaging_migration.py` | Messaging subsystem |
| `fhir_export.py` | FHIR-shaped export |
| `secrets_manager.py`, `secure_transfer.py`, `remove_secrets.py` | Secret handling (Vault-aware) |
| `audit.py`, `audit_docs.py` | Audit helpers |
| `cbt_tools/` (`models.py`, `routes.py`, `utils.py`) | The one already-modularised domain (blueprint pattern to emulate) |
| `create_dev_account.py`, `create_prod_dev_account.py` | **Account-creation scripts (review — §3.2)** |
| `fix_sqlite*.py`, `fix_production*.py`, `refactor_to_postgresql.py`, `phase5_step6_postgresql_fixes.py`, `final_sql_fix.py`, `fix_datetime_functions.py`, `init_postgresql.py`, `comprehensive_sqlite_audit.py` | **One-off DB migration/repair scripts (dead weight; consolidate into authoritative migrations — §5)** |
| `reset_railway_db.py` | **Destructive DB reset script (§3.2)** |

## 3. Database (PostgreSQL, schema defined inline in `api.py`)

- **97 `CREATE TABLE` statements; ~75 distinct tables**, created at app startup (not migrations).
- Key clinical/sensitive tables: `users`, `patients`(via role), `chat_history`, `chat_sessions`,
  `mood_logs`, `wellness_logs`, `risk_alerts`, `risk_assessments`, `risk_reviews`,
  `predictive_risk_flags`, `c_ssrs_assessments`, `safeguarding_concerns`, `safety_plans`,
  `enhanced_safety_plans`, `treatment_plans`, `session_notes`, `clinical_scales`,
  `patient_medications`, `medication_adherence_logs`, `audit_logs`, `data_consent`,
  `ai_monitoring_consent`, `ai_memory*`, `messages`, `message_receipts`, `conversations`,
  `verification_codes`, `crisis_contacts`, `duty_clinician`, `clinician_availability`.
- **No Alembic/Flask-Migrate.** Schema evolution has been done via the `fix_*.py` scripts above.
- Legacy **SQLite** artefacts/logic coexist with Postgres (half-finished migration).

## 4. Environment variables (referenced in code)

Security/danger flags: `ADMIN_WIPE_KEY`, `ALLOW_ADMIN_RESET`, `DEVELOPER_REGISTRATION_KEY`,
`DEBUG`, `TESTING`, `FLASK_ENV`, `RAILWAY_ENVIRONMENT`.
Secrets: `SECRET_KEY`, `CSRF_SECRET`, `ENCRYPTION_KEY`, `PIN_SALT`, `ANONYMIZATION_SALT`,
`GROQ_API_KEY`/`GROQ_API`, `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`, `SMTP_USER`, `SMTP_PASSWORD`,
`SMTP_SERVER`, `SMTP_PORT`, `FROM_EMAIL`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`,
`TWILIO_PHONE_NUMBER`, `VAULT_ADDR`/`HASHICORP_VAULT_ADDR`, `VAULT_TOKEN`.
DB: `DATABASE_URL`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_NAME_PET`.
Other: `ALLOWED_ORIGINS`, `ALERT_WEBHOOK_URL`, `API_URL`, `APP_URL`, `SESSION_COOKIE_DOMAIN`, `PORT`.

## 5. Third-party / external services

| Service | Use | Notes |
|---|---|---|
| **Groq** (`api.groq.com`, `llama-3.3-70b-versatile`) | AI therapy chat + risk context | Only AI provider; REST calls in `api.py` |
| **SMTP / Gmail** | Email (verification, reset, alerts) | Gmail app-password path |
| **Twilio** | **SMS** (alert channel) | Credentials referenced; wiring to verify |
| **Webhook** (`ALERT_WEBHOOK_URL`) | Alert dispatch to external system | To verify |
| **HashiCorp Vault** | Secret retrieval (`secrets_manager.py`) | Optional; falls back to env |
| **Railway** | Hosting/deploy (`railway.toml`, `deploy_railway.sh`, `nixpacks.toml`, `Procfile`) | Single environment observed |
| **edge-tts / pyttsx3** | Text-to-speech (`speech.mp3` artefact tracked) | |

## 6. Notification / alert channels

Email (SMTP/Gmail), SMS (Twilio), outbound webhook, in-app (DB `notifications`,
`message_notifications`, `notification_preferences`). **Email is currently the primary crisis
channel** — spec §11.4 requires it not be the sole acute-risk channel.

## 7. Export & AI-training mechanisms (privacy-critical)

- Export routes: `/api/therapy/export` (POST), `/api/export/fhir` (GET), `/api/export/csv` (GET),
  `/api/export/pdf` (GET), `/api/professional/export-summary` (POST), `/api/training/export` (POST).
- **AI-training pipeline is ACTIVE**: `export_training_data.py` + `training_data_manager.py`
  (self-described "GDPR-compliant training data") + cron installer `setup_training_export_cron.sh`.
  Spec §15.7 requires training export **disabled by default** until governed — currently it is not.

## 8. Scheduled tasks / cron

`setup_cron.sh`, `setup_training_export_cron.sh`, `send_mood_reminders.sh`, `train_scheduler.py`.
No durable job queue (spec §25.1) — work runs in-request or via shell cron.

## 9. Tests

- `tests/` (pytest): `backend/`, `e2e/`, `tier2/`, plus many `tests/test_*.py`.
- Loose root-level `test_*.py` (9 files) outside the configured `testpaths`.
- Baseline (2026-07-19): **805 passed / 129 failed / 71 errored / 17 skipped** — red dominated by
  missing conftest fixtures + no authenticated test DB (see IMPLEMENTATION_STATUS).

## 10. Repository hygiene problems (Phase Zero targets)

Tracked-but-should-not-be: `node_modules/` (884 files), `__pycache__/` + `.pyc` (7),
`backups/` (200 files incl. a repo snapshot `.zip`), `cookies.txt`, `flask.pid`, `speech.mp3`,
`.~lock.*#` LibreOffice locks, `_archive/deprecated-files/*.deb` (110 k lines) + `*.apk`,
`FaviCon.xcf`. Three overlapping archive dirs: `_archive/`, `legacy/`, `backups/`.
