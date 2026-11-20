# Phase 176 R3R17: Public Root Frontier Audit

This read-only package examines the root proof frontier for the registered group query `(n, k) = (3, 5)` after the R3R16 public two-stage connection. It distinguishes a proved zero-image inference from a proved group structure. It does not alter production files, add a GIVEN assertion, assert a group result, or complete the phase.

Run from the repository root in PowerShell after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase176_r3r17_root_frontier_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase176_r3r17_root_frontier_audit\run.ps1"
```

The full audit report is saved to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r17_root_frontier_audit\report.json`.

The audit requires the R3R16 public connection already installed. It uses the current typed public goal and the existing shared expansion provider without injecting conclusions. Four focused tests run with the pytest cache provider disabled. The full test suite is intentionally not run.
