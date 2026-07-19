"""Spec §9: security headers are present on responses.

Note: HSTS and CSP are only emitted when not in DEBUG (production), and the test env runs
with DEBUG=1, so those are covered elsewhere. This asserts the always-on hardening headers,
including the newly added Cross-Origin-Opener-Policy.
"""
import pytest


class TestSecurityHeaders:
    @pytest.fixture
    def resp(self, client):
        return client.get("/api/health")

    def test_x_frame_options_deny(self, resp):
        assert resp.headers.get("X-Frame-Options") == "DENY"

    def test_content_type_options_nosniff(self, resp):
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"

    def test_referrer_policy_present(self, resp):
        assert resp.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_permissions_policy_present(self, resp):
        pp = resp.headers.get("Permissions-Policy")
        assert pp and "geolocation=()" in pp

    def test_coop_same_origin(self, resp):
        assert resp.headers.get("Cross-Origin-Opener-Policy") == "same-origin"
