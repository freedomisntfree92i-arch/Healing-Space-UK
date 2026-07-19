#!/usr/bin/env python3
"""Parse api.py and emit a route security matrix (markdown table + summary)."""
import re, sys

SRC = __import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'api.py')
lines = open(SRC, encoding="utf-8", errors="replace").read().split("\n")

route_re = re.compile(r"@app\.route\(\s*['\"]([^'\"]+)['\"](?:.*methods\s*=\s*\[([^\]]*)\])?")
routes = []
i = 0
n = len(lines)
while i < n:
    m = route_re.search(lines[i])
    if not m:
        i += 1
        continue
    path = m.group(1)
    methods = m.group(2)
    if methods:
        methods = ",".join(re.findall(r"['\"]([A-Z]+)['\"]", methods))
    else:
        methods = "GET"
    # collect decorators between this route line and the def
    deco_start = i
    # walk back to include decorators above the route (rare) - not needed
    # walk forward: decorators + def
    j = i + 1
    decos = []
    func = None
    while j < n and j < i + 12:
        s = lines[j].strip()
        if s.startswith("@"):
            decos.append(s)
        elif s.startswith("def "):
            func = s[4:].split("(")[0]
            def_line = j
            break
        j += 1
    # capture body until next @app.route or top-level def or EOF (cap 200 lines)
    body_start = j
    k = j + 1
    body = []
    while k < n and k < body_start + 220:
        if lines[k].startswith("@app.route") or (lines[k].startswith("def ") ):
            break
        body.append(lines[k])
        k += 1
    body_text = "\n".join(body)
    all_deco = "\n".join(decos)
    csrf = "CSRFProtection" in all_deco or "require_csrf" in all_deco
    ratelimit = "check_rate_limit" in all_deco or "limiter.limit" in all_deco
    authn = ("get_authenticated_username" in body_text or "session.get('user" in body_text
             or "session['user" in body_text or "current_user" in body_text)
    role = bool(re.search(r"role.{0,40}(clinician|developer|admin|patient)", body_text)
                or "require_role" in body_text or "SELECT role FROM users" in body_text)
    patient_rel = "verify_clinician_patient_relationship" in body_text
    state_changing = any(x in methods for x in ("POST", "PUT", "PATCH", "DELETE"))
    routes.append(dict(line=deco_start+1, path=path, methods=methods, func=func or "?",
                       csrf=csrf, rate=ratelimit, authn=authn, role=role,
                       prel=patient_rel, state=state_changing))
    i = k

# ---- Summary ----
total = len(routes)
state = [r for r in routes if r["state"]]
def yn(b): return "Y" if b else "-"

state_no_csrf = [r for r in state if not r["csrf"]]
state_no_authn = [r for r in state if not r["authn"]]
no_rate = [r for r in routes if not r["rate"]]
clinician_no_prel = [r for r in routes if r["role"] and not r["prel"] and ("patient" in r["path"] or "clinician" in r["path"])]

print("# Route Security Matrix — Healing Space UK")
print("\n_Auto-generated from `api.py` by `scripts/gen_route_matrix.py`. Heuristic — the authN/role/")
print("patient-rel columns are detected by scanning each handler body and REQUIRE manual confirmation")
print("during the per-domain refactor (spec §4). Regenerate after each refactor phase._\n")
print("## IMPORTANT — how enforcement actually works (verified, not per-decorator)\n")
print("- **CSRF is enforced GLOBALLY** via `@app.before_request csrf_protect()` (api.py:2414), not per")
print("  route. The `CSRF` column below only marks the per-route `@CSRFProtection` decorator and is NOT")
print("  the source of truth. **However the global validator is BROKEN**: `validate_csrf_token()`")
print("  (api.py:~2379) accepts ANY 64-char alphanumeric string and is fully bypassed when `TESTING=1`.")
print("  The token is not session-bound. See SECURITY_FINDINGS SEC-001. Treat ALL state-changing routes")
print("  as effectively CSRF-unprotected until SEC-001 is fixed.")
print("- **Rate limiting**: a global Flask-Limiter default (`200/day, 50/hour`, `storage_uri=memory://`)")
print("  applies to all routes; a second custom in-memory `RateLimiter` guards 12 sensitive endpoints via")
print("  `@check_rate_limit`. Neither is distributed (SEC-003). The `rate` column marks only the custom one.")
print("- **AuthN/role/patient-rel** are enforced INLINE inside handlers (`get_authenticated_username()`,")
print("  `SELECT role FROM users`, `verify_clinician_patient_relationship()`), never via decorators — so")
print("  coverage cannot be guaranteed by inspection and must be centralised (spec §7).\n")
print(f"- Total routes parsed: **{total}**")
print(f"- State-changing (POST/PUT/PATCH/DELETE): **{len(state)}**")
print(f"- State-changing WITHOUT CSRF decorator: **{len(state_no_csrf)}**")
print(f"- State-changing WITHOUT detectable authN: **{len(state_no_authn)}**")
print(f"- Routes WITHOUT rate limiting: **{len(no_rate)}** of {total}")
print(f"- Clinician/patient routes WITHOUT patient-relationship check: **{len(clinician_no_prel)}**\n")

print("## State-changing routes missing CSRF (HIGH PRIORITY)\n")
print("| Line | Method | Path | Func | authN | role |")
print("|---|---|---|---|---|---|")
for r in sorted(state_no_csrf, key=lambda x: x["line"]):
    print(f"| {r['line']} | {r['methods']} | `{r['path']}` | {r['func']} | {yn(r['authn'])} | {yn(r['role'])} |")

print("\n## State-changing routes with NO detectable authentication (CRITICAL to review)\n")
print("| Line | Method | Path | Func | csrf |")
print("|---|---|---|---|---|")
for r in sorted(state_no_authn, key=lambda x: x["line"]):
    print(f"| {r['line']} | {r['methods']} | `{r['path']}` | {r['func']} | {yn(r['csrf'])} |")

print("\n## FULL MATRIX\n")
print("| Line | Method | Path | authN | role | patient-rel | CSRF | rate |")
print("|---|---|---|---|---|---|---|---|")
for r in sorted(routes, key=lambda x: x["line"]):
    print(f"| {r['line']} | {r['methods']} | `{r['path']}` | {yn(r['authn'])} | {yn(r['role'])} | {yn(r['prel'])} | {yn(r['csrf'])} | {yn(r['rate'])} |")
