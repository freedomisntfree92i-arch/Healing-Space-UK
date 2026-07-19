"""SEC-001 regression tests: CSRF is session-bound and actually enforced.

The old validator accepted ANY 64-char alphanumeric string and was bypassed under
TESTING. These tests flip TESTING off so the REAL validator runs, and prove:
  - a state-changing request with no / wrong / foreign token is rejected (403 CSRF_FAILED);
  - a request carrying the session-bound token passes the CSRF gate;
  - an arbitrary 64-char string (the old bypass) no longer validates;
  - production refuses to start with TESTING enabled.

We use a non-exempt state-changing endpoint (`POST /api/cbt/goals`). The CSRF check runs
in a before_request hook, so it is reached before authentication.
"""
import os
import sys
import subprocess

import pytest

PROTECTED_POST = "/api/cbt/goals"


def _csrf_failed(resp):
    if resp.status_code != 403:
        return False
    try:
        return resp.get_json(silent=True).get("code") == "CSRF_FAILED"
    except AttributeError:
        return False


@pytest.fixture
def csrf_enforced(monkeypatch):
    """Turn the TESTING bypass off so the real CSRF validator runs."""
    monkeypatch.setenv("TESTING", "0")
    yield


class TestCsrfEnforced:
    def test_missing_token_rejected(self, client, csrf_enforced):
        resp = client.post(PROTECTED_POST, json={"title": "x"})
        assert _csrf_failed(resp), f"expected CSRF_FAILED 403, got {resp.status_code}"

    def test_wrong_token_rejected(self, client, csrf_enforced):
        client.get("/api/csrf-token")  # establishes a session token
        resp = client.post(
            PROTECTED_POST, json={"title": "x"},
            headers={"X-CSRF-Token": "b" * 64},
        )
        assert _csrf_failed(resp), f"expected CSRF_FAILED 403, got {resp.status_code}"

    def test_old_bypass_string_no_longer_validates(self, client, csrf_enforced):
        """The exact shape the old code accepted: 64-char alphanumeric, but not the
        session token. Must now be rejected."""
        client.get("/api/csrf-token")
        bogus = "a1" * 32  # 64 chars, isalnum() == True
        assert len(bogus) == 64 and bogus.isalnum()
        resp = client.post(
            PROTECTED_POST, json={"title": "x"},
            headers={"X-CSRF-Token": bogus},
        )
        assert _csrf_failed(resp), "old 64-char-alnum bypass still works — SEC-001 not fixed"

    def test_valid_session_token_passes_csrf_gate(self, client, csrf_enforced):
        token = client.get("/api/csrf-token").get_json()["csrf_token"]
        resp = client.post(
            PROTECTED_POST, json={"title": "x"},
            headers={"X-CSRF-Token": token},
        )
        # It may still fail later for auth reasons, but it must NOT be a CSRF rejection.
        assert not _csrf_failed(resp), "valid session token was rejected by CSRF gate"

    def test_token_is_session_bound(self, app, csrf_enforced):
        """A token issued to one session must not validate for a different session."""
        c1 = app.test_client()
        c2 = app.test_client()
        t1 = c1.get("/api/csrf-token").get_json()["csrf_token"]
        # c2 has its own (different) session token; submitting c1's token to c2 must fail.
        resp = c2.post(PROTECTED_POST, json={"title": "x"}, headers={"X-CSRF-Token": t1})
        assert _csrf_failed(resp), "cross-session token was accepted"

    def test_csrf_token_endpoint_returns_both_keys(self, client):
        data = client.get("/api/csrf-token").get_json()
        assert data.get("csrf_token") and data.get("token"), "endpoint must return csrf_token + token"
        assert data["csrf_token"] == data["token"]


class TestProductionTestingGuard:
    def test_production_refuses_testing_mode(self):
        """Importing the app with FLASK_ENV=production and TESTING=1 must fail fast."""
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        env = dict(os.environ)
        env.update({
            "FLASK_ENV": "production", "TESTING": "1", "DEBUG": "",
            "SECRET_KEY": "x" * 40, "PIN_SALT": "x", "GROQ_API_KEY": "x",
            "ENCRYPTION_KEY": "dGVzdGtleQ==",
        })
        proc = subprocess.run(
            [sys.executable, "-c", "import api"],
            cwd=root, env=env, capture_output=True, text=True,
        )
        assert proc.returncode != 0, "app started with TESTING=1 in production"
        assert "TESTING=1 is not permitted" in (proc.stderr + proc.stdout)
