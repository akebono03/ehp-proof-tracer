Phase 164 R6 static unification audit.
Extract this folder directly into the ehp_proof repository root.
Run: powershell -ExecutionPolicy Bypass -File .\phase164_r6_unification_audit\run.ps1
Output: phase164_r6_output\report.md and audit.json
Existing source and tests are NOT modified. No pytest is run.
The report indexes top-level Python modules and tests outside archive folders; it is not a proof that any code is safe to delete.
