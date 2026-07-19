# External Assurance Required — Healing Space UK

_Items that **code cannot satisfy**. For each, engineering prepares everything technically necessary
and the correct evidence structure, then marks it `IMPLEMENTED — EXTERNAL REVIEW OR APPROVAL
REQUIRED`. **No approval, date, name, trial, or result may be fabricated** (spec preamble)._

| # | Item | What engineering delivers | What only a qualified human/body can do |
|---|---|---|---|
| EXT-1 | **Clinical safety (DCB0129/DCB0160)** | Hazard log, clinical safety plan, escalation model, evidence index | Named **Clinical Safety Officer** ownership + sign-off |
| EXT-2 | **DTAC assessment** | DTAC evidence index mapping controls to code | NHS/commissioner DTAC review outcome |
| EXT-3 | **NHS acceptance / deployment** | Technical readiness, interoperability scoping | NHS organisation acceptance decision |
| EXT-4 | **DPIA + IG sign-off** | DPIA draft, lawful-basis register, RoPA, subprocessor register | Data Protection Officer / IG review + approval |
| EXT-5 | **Independent penetration test** | Threat model, hardening, self-tests, remediation of internal findings | Independent CREST-equivalent pen test + report |
| EXT-6 | **Independent accessibility audit** | WCAG 2.2 AA implementation + automated axe checks + manual test plan | External accessibility audit + statement |
| EXT-7 | **Clinical validation of instruments/AI** | Correct scoring impl + golden-vector tests + AI boundaries | Clinical/psychometric validation study |
| EXT-8 | **Ethics approval (if research)** | Research export workflow, consent versioning, protocol fields | Research ethics committee approval |
| EXT-9 | **Medical-device determination** | Intended-purpose statement, AI clinical boundaries | Regulatory (MHRA) classification decision |
| EXT-10 | **Legal review** | Draft policies, disclaimers, terms | Qualified legal counsel review |
| EXT-11 | **Backup/DR recoverability** | Encrypted backups, restore runbook, RPO/RTO targets | An actual tested restore in a real environment |
| EXT-12 | **Secret rotation** | Rotation runbook + exact checklist of every exposed secret | The user rotating creds in Railway/Gmail/Groq/Twilio dashboards |

## Standing rule
Every public/user-facing surface must reflect these as *pending/required*, never as *held*.
Placeholders in generated docs use: `TO BE COMPLETED BY AUTHORISED HUMAN REVIEWER`.
