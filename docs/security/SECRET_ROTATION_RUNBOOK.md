# Secret Rotation Runbook — Healing Space UK

> **Rotation is a HUMAN action performed outside this repository.** This runbook lists exactly
> what to rotate and how. Nothing here may be marked "done" by code. Do not commit any real secret.

## 🔴 URGENT — confirmed exposed credential (rotate immediately)

A **real PostgreSQL production password** was committed to git history and remained in the working
tree under `backups/` until Phase Zero untracked it:

```
postgresql://postgres:zkzFIlnbBIFNTomTawKPymiZwhWpvYfG@postgres.railway.internal:5432/railway
```
- **Files (history):** `backups/documentation_feb8_2026/documentation/archive/PROJECT_COMPLETION_PHASE_1_5.md`
  and related `backups/.../infra_and_deployment/*.md`.
- **Action NOW (you, in Railway):** rotate the Postgres password / recreate the database credential,
  then update `DATABASE_URL` in the Railway environment. Assume the old password is compromised.
- Untracking from HEAD does **not** remove it from history — a history purge is still required
  (see `REPOSITORY_EXPOSURE_RESPONSE.md`). The password stays valid until you rotate it.

## Full rotation checklist

For each secret: rotate at the provider → update the deployment env (Railway) → verify the app →
invalidate the old value. Tick only after the provider shows the new value live.

| Secret / env var | Provider / where to rotate | Status |
|---|---|---|
| `DATABASE_URL` (Postgres password) | Railway → Postgres plugin → rotate credentials | ☐ **URGENT** |
| `GROQ_API_KEY` | console.groq.com → API keys → revoke + create | ☐ |
| `SECRET_KEY` (Flask session signing) | Generate `python -c "import secrets;print(secrets.token_hex(32))"`; set in Railway | ☐ (rotating logs users out) |
| `CSRF_SECRET` | Same generation; set in Railway | ☐ (do after SEC-001 CSRF fix) |
| `ENCRYPTION_KEY` (Fernet) | ⚠️ **Do NOT blind-rotate** — rotating breaks decryption of existing data. Plan key-migration (envelope/re-encrypt) first (§17). | ☐ blocked on §17 |
| `PIN_SALT`, `ANONYMIZATION_SALT` | ⚠️ Same caveat — changing invalidates existing hashes/pseudonyms. Plan migration. | ☐ blocked |
| `GMAIL_APP_PASSWORD` / `SMTP_PASSWORD` | Google Account → App passwords → revoke + create | ☐ |
| `TWILIO_AUTH_TOKEN` | Twilio console → rotate auth token | ☐ |
| `ADMIN_WIPE_KEY`, `ALLOW_ADMIN_RESET`, `DEVELOPER_REGISTRATION_KEY` | No longer used by removed routes (SEC-002) — **delete** from Railway env | ☐ |
| `VAULT_TOKEN` | HashiCorp Vault → revoke + reissue | ☐ (if Vault used) |

## Notes
- Placeholders found in history (`gsk_xxxx`, `PASSWORD`, `your_pin_salt_here`) are **not** live
  secrets — no rotation needed for those specific strings, but rotate the real values above.
- After rotation, run the app against the new values in staging before production cutover.
- Keep this file updated as each item is rotated; do not record the secret values here.
