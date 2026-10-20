# Phase 166 R3-Q Reference Audit

This package diagnoses how the published order changes available typed Reference proof leaves for the pi3^2 group goal. Run from the repository root with PowerShell. This is a read-only production-code audit: it only writes `phase166_r3q_reference_audit_results/audit.json`. It does not change proof selection, statement registries, renderers, or tests and does not run full pytest.

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3q_reference_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3q_reference_audit\run.ps1"
```
