# Running Healing Space UK locally

The app is a Flask backend (`api.py`) backed by PostgreSQL. `.env` is auto-loaded
(`python-dotenv`). It creates its tables at startup (`init_db()`).

## Quick start (helper script)

```bash
./scripts/dev_run.sh
```

This creates a `venv`, installs `requirements.txt`, generates a git-ignored `.env` with safe
DEV secrets (strong `SECRET_KEY`, a valid Fernet `ENCRYPTION_KEY`, salts, placeholder Groq key),
and starts the app on http://localhost:5000. You still need a PostgreSQL database (below).

## Manual steps

1. **PostgreSQL** — create a database + user matching your `.env`:
   ```bash
   sudo -u postgres psql -c "CREATE USER healing_space WITH PASSWORD 'healing_space_dev_pass';"
   sudo -u postgres psql -c "CREATE DATABASE healing_space OWNER healing_space;"
   ```

2. **Virtualenv + deps**:
   ```bash
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment** — copy the example and fill required values:
   ```bash
   cp .env.example .env
   ```
   Minimum required to boot (enforced at startup):
   - `DEBUG=1`
   - `DATABASE_URL=postgresql://healing_space:healing_space_dev_pass@localhost:5432/healing_space`
     (or the individual `DB_HOST`/`DB_PORT`/`DB_NAME_PET`/`DB_USER`/`DB_PASSWORD` vars)
   - `SECRET_KEY` — **32+ chars** (`python -c "import secrets; print(secrets.token_hex(32))"`)
   - `ENCRYPTION_KEY` — a **Fernet key** (`python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`)
   - `PIN_SALT`, `ANONYMIZATION_SALT` — any random strings
   - `GROQ_API_KEY` — a real `gsk_...` key for AI chat; a placeholder still lets the app boot in DEBUG.

4. **Run**:
   ```bash
   python api.py            # dev server on http://localhost:5000
   # or, closer to production:
   gunicorn api:app         # (Procfile uses this)
   ```

## Running the tests

```bash
pip install pytest pytest-timeout pytest-mock
python -m pytest tests/ -o addopts="" -q
```
Most tests mock the database; some need a `healing_space_test` DB. The known baseline is
~837 passing with ~129 pre-existing failures/71 errors caused by incomplete test-harness
fixtures (tracked under spec §26) — not product regressions.

## Notes / gotchas
- `TESTING=1` disables CSRF and is **refused at startup** in production/non-DEBUG (SEC-001).
- CSRF **cannot** be disabled by env (the old `DISABLE_CSRF` key was dead and has been removed).
- AI-training data collection/export is **off by default** (`TRAINING_DATA_ENABLED`, PRIV-001).
- Never commit your `.env` — it is git-ignored.
