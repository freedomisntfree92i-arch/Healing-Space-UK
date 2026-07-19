"""Phase Zero SEC-002 regression guard.

The destructive HTTP endpoints that could reset/wipe the clinical database have been
removed. These tests assert they stay gone: a request to them must NOT reach a handler
(Flask returns 404/405 for an unregistered rule). If someone re-adds one of these routes,
these tests fail.
"""
import pytest


REMOVED_GET_ROUTES = [
    "/api/admin/wipe",
    "/api/debug/analytics/somebody",
]

REMOVED_POST_ROUTES = [
    "/api/admin/wipe-database",
    "/api/admin/reset-users",
]


class TestDestructiveRoutesRemoved:
    @pytest.mark.parametrize("path", REMOVED_GET_ROUTES)
    def test_removed_get_routes_return_404(self, client, path):
        resp = client.get(path)
        assert resp.status_code == 404, (
            f"{path} should be removed (404) but returned {resp.status_code}"
        )

    @pytest.mark.parametrize("path", REMOVED_POST_ROUTES)
    def test_removed_post_routes_not_registered(self, client, path):
        # An unregistered path returns 404; a wrong method on a registered path
        # returns 405. Either way it must not be a live POST handler (2xx/3xx/403/500).
        resp = client.post(path, json={})
        assert resp.status_code in (404, 405), (
            f"{path} should not be a live handler but returned {resp.status_code}"
        )

    def test_destructive_rules_absent_from_url_map(self, app):
        rules = {r.rule for r in app.url_map.iter_rules()}
        for bad in ("/api/admin/wipe", "/api/admin/wipe-database", "/api/admin/reset-users"):
            assert bad not in rules, f"{bad} is still registered in the URL map"
        assert not any("debug/analytics" in r for r in rules), "debug/analytics still registered"
