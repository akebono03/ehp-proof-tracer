# Phase 176 R3R11 — Isolated-to-Shared Bridge Evidence Audit

This read-only package inventories the prior R3R10 report and reviews the existing shared composite-zero provider. It does not add a proof rule, GIVEN, provider, or completed group proof.

Run from the repository root after extracting the ZIP:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase176_R3R11_Isolated_Shared_Bridge_Audit.zip" -DestinationPath "." -Force
$script = ".\phase176_r3r11_isolated_shared_bridge_audit\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R11 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R11 audit failed" }
git diff --check
git diff --stat
git status -sb
```

The source repository and R3R10 report are required. The output is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r11_isolated_shared_bridge_audit\report.json`.

The report records the actual nested JSON keys and scalar evidence, as well as static guard conditions for the existing public provider. Prior R3R10 values shown in the console are clearly marked as prior console evidence and not re-measured. This stage does **not** establish the precise mathematical cause of zero shared candidates.

The focused test run includes four local tests plus existing public-provider tests. The full test suite is intentionally not run before Phase closeout.
