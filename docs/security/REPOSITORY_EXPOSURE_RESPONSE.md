# Repository Exposure Response — Healing Space UK

_How to respond to secrets/PII found in the repo or its history. Written during Phase Zero
(2026-07-19) after a confirmed exposure._

## Confirmed exposures (2026-07-19 scan)

| Item | Location | Severity | Response |
|---|---|---|---|
| Railway Postgres password `zkzFIlnbBIFNTomTawKPymiZwhWpvYfG` | git history + `backups/.../PROJECT_COMPLETION_PHASE_1_5.md` | **CRITICAL** | Rotate now (runbook) + purge history |
| Railway DB URL with redacted `***` | `backups/.../DATABASE_SCHEMA_FIXES_FEB5_2026.md` | LOW (redacted) | Purge with backups/ |
| `cookies.txt` (session cookie) tracked | repo root (now untracked) | MEDIUM | Ensure session rotated; keep untracked |
| Placeholder keys (`gsk_xxxx`, `your_*`) | `.env.example`, `backups/*` docs | INFO | No live secret; leave example, purge backups |

## Immediate response (done in Phase Zero)
1. ✅ Untracked `backups/`, `cookies.txt`, and other junk from the index (files remain on disk).
2. ✅ Added `backups/` and secret patterns to `.gitignore` so they cannot be re-added.
3. ✅ Documented the exact credential to rotate (`SECRET_ROTATION_RUNBOOK.md`).
4. ☐ **YOU:** rotate the Railway Postgres password (only you can do this).

## History purge (planned — DECISION: verify first, then purge)
The exposed password remains in historical commits until history is rewritten. Because this repo is
**solo (no other clones)**, a rewrite is low-risk to coordinate.

Recommended tool: `git filter-repo` (preferred over BFG for path+blob control).
```
# DRY RUN FIRST — review, then run for real, then force-push, then everyone re-clones.
pip install git-filter-repo
# remove the whole backups/ tree and known secret-bearing paths from ALL history:
git filter-repo --path backups/ --path cookies.txt --invert-paths
# also strip the literal password string from any remaining blobs:
git filter-repo --replace-text <(echo 'zkzFIlnbBIFNTomTawKPymiZwhWpvYfG==>REDACTED')
```
Do **not** run the purge until: (a) the password is rotated, and (b) you confirm no other working
copy needs preserving. After purge: `git push --force-with-lease` to the canonical remote.

> ⚠️ Remote note: local remote is `shadowWolf88/Healing-Space-UK`; the remediation spec referenced
> `freedomisntfree92i-arch`. Confirm the canonical remote before any force-push.

## Standing procedure for future exposures
1. Treat the secret as compromised — rotate first, investigate second.
2. Untrack + gitignore the file; never `git rm` alone (history retains it).
3. Record it in this file; decide on history purge.
4. Add a secret-scanning CI gate (`gitleaks`/`trufflehog`) so it cannot recur (§24.2).
