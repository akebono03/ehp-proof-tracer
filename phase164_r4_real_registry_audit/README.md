# Phase 164 R4 — Real Registry and Legacy Proof Audit

This package adds a read-only audit module and focused tests. It does not modify existing production behavior, the Phase 161 backward search, or the Phase 162 renderer.

Run from the repository root (PowerShell):

```powershell
Expand-Archive -Path "$HOME\Downloads\phase164_r4_real_registry_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase164_r4_real_registry_audit\run.ps1"
```

The audit checks the actual Phase 163 R94 manifest and production registry bridge. It independently reconstructs the existing pi_5^3 proof from the established Phase 59 test witness data, validates the Phase 161 R7 proof ancestry, and renders it using the existing Phase 162 renderer. This baseline must not be confused with authorization of any archival statement.

Outputs: `phase164_r4_output/report.json`, `report.md`, and `legacy_narrative.md`.

The R94 archive contains 108 references and 117 assertions with zero mathematical verification or proof eligibility. The audit deliberately does not invent a citing assertion ID, verified assertion allowlist, or publication positions; real-registry R3 authorization remains blocked pending independent evidence. R5 is the phase-closing audit. The full test suite is not run in R4.
