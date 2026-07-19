"""Spec §8.2: CORS must not reflect an arbitrary Origin with credentials.

The test env runs in DEBUG with no ALLOWED_ORIGINS, so the local dev allowlist applies
(localhost + Capacitor). A disallowed Origin must NOT be echoed back in
Access-Control-Allow-Origin. Also verifies the DEBUG-in-production startup guard.
"""
import os
import sys
import subprocess


class TestCorsAllowlist:
    def test_disallowed_origin_not_reflected(self, client):
        resp = client.get("/api/health", headers={"Origin": "http://evil.example.com"})
        acao = resp.headers.get("Access-Control-Allow-Origin")
        assert acao != "http://evil.example.com", "arbitrary Origin reflected with credentials"

    def test_allowed_dev_origin_permitted(self, client):
        resp = client.get("/api/health", headers={"Origin": "http://localhost:5000"})
        acao = resp.headers.get("Access-Control-Allow-Origin")
        # flask-cors echoes an allowed origin; must be the specific origin, never "*" with creds.
        assert acao in ("http://localhost:5000", None)
        assert acao != "*"


class TestDebugInProductionGuard:
    def test_production_refuses_debug(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        env = dict(os.environ)
        env.pop("TESTING", None)
        env.update({
            "FLASK_ENV": "production", "DEBUG": "1",
            "SECRET_KEY": "x" * 40, "PIN_SALT": "x", "GROQ_API_KEY": "x",
            "ENCRYPTION_KEY": "dGVzdGtleQ==",
        })
        proc = subprocess.run(
            [sys.executable, "-c", "import api"],
            cwd=root, env=env, capture_output=True, text=True,
        )
        assert proc.returncode != 0
        assert "DEBUG must not be enabled" in (proc.stderr + proc.stdout)
