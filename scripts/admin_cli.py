#!/usr/bin/env python3
"""
Offline administrative CLI for Healing Space UK.

Replaces the removed destructive HTTP endpoints (Phase Zero SEC-002):
  - POST /api/admin/wipe-database
  - POST /api/admin/reset-users

These operations are DESTRUCTIVE and irreversible. They are intentionally NOT
reachable over HTTP. They run only from a shell with direct infrastructure access,
refuse to run against production, and require typed human confirmation.

Usage:
    python scripts/admin_cli.py wipe-database   # clears clinical data tables
    python scripts/admin_cli.py reset-users     # deletes all users + related data

Guards:
  * Refuses to run if FLASK_ENV=production or RAILWAY_ENVIRONMENT=production,
    UNLESS ADMIN_CLI_ALLOW_PROD=1 is explicitly exported (break-glass, audited).
  * Requires the operator to type the exact confirmation phrase.
  * Prints affected row counts and writes an audit event.
"""
import os
import sys

CONFIRM_PHRASE = "DELETE ALL DATA"

WIPE_DATABASE_TABLES = [
    "users", "patient_approvals", "chat_history", "chat_sessions", "mood_logs",
    "alerts", "notifications", "clinical_scales", "cbt_records", "ai_memory",
    "appointments", "audit_logs", "verification_codes",
]

RESET_USERS_TABLES = [
    "users", "patient_approvals", "notifications", "sessions", "chat_history",
    "mood_logs", "gratitude_logs", "cbt_records", "clinical_scales",
    "safety_plans", "ai_memory", "community_posts", "alerts",
]


def _is_production() -> bool:
    return (
        os.environ.get("FLASK_ENV") == "production"
        or os.environ.get("RAILWAY_ENVIRONMENT") == "production"
    )


def _guard():
    if _is_production() and os.environ.get("ADMIN_CLI_ALLOW_PROD") != "1":
        sys.exit(
            "REFUSED: this is a production environment. Destructive admin operations "
            "are blocked. If you truly intend this, export ADMIN_CLI_ALLOW_PROD=1 and "
            "re-run (this is an audited break-glass action)."
        )


def _confirm(action: str, tables):
    print(f"\n*** DESTRUCTIVE ACTION: {action} ***")
    print("This will DELETE all rows from:")
    print("  " + ", ".join(tables))
    print(f"\nEnvironment: FLASK_ENV={os.environ.get('FLASK_ENV', '(unset)')} "
          f"RAILWAY_ENVIRONMENT={os.environ.get('RAILWAY_ENVIRONMENT', '(unset)')}")
    typed = input(f'\nType exactly "{CONFIRM_PHRASE}" to proceed (anything else aborts): ')
    if typed != CONFIRM_PHRASE:
        sys.exit("Aborted — confirmation phrase did not match. No changes made.")


def _run(action: str, tables):
    _guard()
    _confirm(action, tables)

    # Import api lazily so the module-level guards above run first.
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    import api  # noqa: E402

    conn = api.get_db_connection()
    cur = api.get_wrapped_cursor(conn)
    results = {}
    for table in tables:
        try:
            cur.execute(f"DELETE FROM {table}")
            results[table] = cur.rowcount
            print(f"  cleared {table}: {cur.rowcount} rows")
        except Exception as exc:  # noqa: BLE001
            results[table] = f"error: {exc}"
            print(f"  WARN {table}: {exc}")
    conn.commit()
    try:
        api.log_event("ADMIN_CLI", "admin", action, f"offline CLI: {results}")
    except Exception:  # noqa: BLE001
        pass
    conn.close()
    print(f"\n{action} complete.")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("wipe-database", "reset-users"):
        sys.exit(__doc__)
    if sys.argv[1] == "wipe-database":
        _run("wipe-database", WIPE_DATABASE_TABLES)
    else:
        _run("reset-users", RESET_USERS_TABLES)


if __name__ == "__main__":
    main()
