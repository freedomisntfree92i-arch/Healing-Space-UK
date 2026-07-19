# Security Policy — Healing Space UK

Healing Space UK handles sensitive mental-health data. We take security and
clinical-safety reports seriously.

## Reporting a vulnerability

**Do not open a public issue for security vulnerabilities.**

Report privately via GitHub's **"Report a vulnerability"** (Security → Advisories)
or email the maintainer at: `TO BE COMPLETED BY AUTHORISED HUMAN REVIEWER`.

Please include:
- a description of the issue and its impact,
- steps to reproduce (proof-of-concept if possible),
- affected component/route/version.

We aim to acknowledge reports within **3 working days**. This is a best-effort
target for a project in active remediation, not a contractual SLA.

## Scope

In scope: authentication/authorisation, CSRF, injection, IDOR, data exposure,
crisis/safeguarding workflow integrity, AI safety, mobile wrapper security.

## Safe-harbour

We will not pursue action against good-faith researchers who:
- avoid privacy violations and service disruption,
- do not access, modify or delete real patient data,
- give us reasonable time to remediate before disclosure.

## Data-handling note

If a report involves real patient data exposure, **do not download or retain it**.
Describe the exposure and stop. See `docs/security/REPOSITORY_EXPOSURE_RESPONSE.md`.
