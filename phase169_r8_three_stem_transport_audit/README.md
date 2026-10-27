# Phase 169 R8 — Three-Stem Transport Dependency Audit

This is a read-only diagnostic for the unfinished `pi_10^7` group proof. It **does not** install a new rule, patch the production provider, promote database goals to proof facts, or run a full pytest suite.

Run from the repository root using Windows PowerShell:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r8_three_stem_transport_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r8_three_stem_transport_audit\run.ps1"
```

Output is written only to `phase169_r8_three_stem_transport_audit/output/audit.json` and `output/audit.md`.

This audit examines current typed goals and proof-search statuses for `pi_8^5`, `pi_9^6`, and `pi_10^7`; publication eligibility of preceding 3-stem group records; R7 candidate generation and one-step generator image obligations. It does not claim completion merely because it can generate typed candidate subgoals.

The audit imports existing application code and performs three targeted proof searches, so the runtime depends on the user's local checkout and its installed dependencies. It never modifies application files or existing tests. The full suite remains reserved for the end of Phase 169.
