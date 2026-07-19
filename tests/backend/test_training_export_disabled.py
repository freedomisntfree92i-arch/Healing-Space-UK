"""PRIV-001 (spec §15.7): AI-training data export/collection is disabled by default.

Clinical data must not flow into a training corpus until a governed workflow exists.
These tests assert the /api/training/export endpoint refuses by default and only becomes
reachable when an operator explicitly enables TRAINING_DATA_ENABLED.
"""
import pytest

import api


def _code(resp):
    body = resp.get_json(silent=True) or {}
    return body.get("code")


class TestTrainingExportDisabled:
    def test_flag_defaults_off(self):
        # Enabled only by explicit operator opt-in; must be falsey in a default/test env.
        assert api.TRAINING_DATA_ENABLED is False

    def test_export_refused_by_default(self, client, monkeypatch):
        monkeypatch.setattr(api, "TRAINING_DATA_ENABLED", False)
        resp = client.post("/api/training/export", json={"username": "alice"})
        assert resp.status_code == 403
        assert _code(resp) == "TRAINING_EXPORT_DISABLED"

    def test_refusal_happens_before_consent_or_username_logic(self, client, monkeypatch):
        # Even with no username, the disabled-guard fires first (not the 400 username error).
        monkeypatch.setattr(api, "TRAINING_DATA_ENABLED", False)
        resp = client.post("/api/training/export", json={})
        assert resp.status_code == 403
        assert _code(resp) == "TRAINING_EXPORT_DISABLED"

    def test_endpoint_reachable_only_when_explicitly_enabled(self, client, monkeypatch):
        # When enabled, the disabled-guard no longer fires; it proceeds to consent/username
        # logic (which will reject this unconsented/unknown user) — but NOT with the
        # disabled code. This proves the gate is the flag, nothing else.
        monkeypatch.setattr(api, "TRAINING_DATA_ENABLED", True)
        resp = client.post("/api/training/export", json={"username": "nonexistent_user"})
        assert _code(resp) != "TRAINING_EXPORT_DISABLED"
