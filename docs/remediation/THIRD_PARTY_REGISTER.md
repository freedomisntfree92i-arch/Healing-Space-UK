# Third-Party / Subprocessor Register — Healing Space UK

_Actual external dependencies found in code (2026-07-19). Data-protection detail (region,
retention, DPA/subprocessor status) is **NEEDS-INPUT** — to be completed with contractual evidence
in Phase §16/§28. Do not assert a DPA exists without the signed agreement._

| Service | Category | Data sent | Region/DPA | Evidence status |
|---|---|---|---|---|
| **Groq** (`api.groq.com`, model `llama-3.3-70b-versatile`) | LLM inference (therapy chat, risk context) | Patient message text, memory/context, risk prompts — **special-category health data** | NEEDS-INPUT (hosting region, retention, training policy) | Model registry required (§15.3); confirm no-training + retention in contract |
| **Twilio** | SMS alert channel | Recipient phone, alert content (should be minimal) | NEEDS-INPUT | Confirm approved for clinical alerting; minimise message content |
| **Google / Gmail SMTP** | Transactional email (verification, reset, alerts) | Email address, links, alert notices | NEEDS-INPUT | Confirm no clinical content in email bodies (§16.7) |
| **Outbound webhook** (`ALERT_WEBHOOK_URL`) | Alert forwarding to monitored system | Alert payload | NEEDS-INPUT | Confirm endpoint auth + payload minimisation |
| **HashiCorp Vault** | Secret retrieval | Secrets only (no patient data) | Self-hosted (optional) | Verify prod usage vs env fallback |
| **Railway** | Hosting / PaaS + Postgres | All application + DB data | NEEDS-INPUT | Confirm data residency, encryption, backups (§17/§25) |
| **edge-tts / pyttsx3** | Text-to-speech | Text to synthesise (edge-tts is a Microsoft online service) | NEEDS-INPUT | edge-tts sends text to Microsoft — assess for clinical content leakage |
| **cdn.jsdelivr.net** | Frontend asset CDN (in CSP `connect-src`) | None (static assets) | Public CDN | Prefer self-hosting for strict CSP (§9) |

## Actions
- Build `docs/privacy/SUBPROCESSOR_REGISTER.md` (§28) from this with contractual evidence.
- **edge-tts** and **Groq** both transmit potentially sensitive text off-platform — assess in DPIA.
- No analytics/marketing SDK found in the sampled sweep — confirm during frontend refactor (§19/§22.2).
