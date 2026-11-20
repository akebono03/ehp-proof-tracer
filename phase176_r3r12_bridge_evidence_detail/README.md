# Phase 176 R3R12 — Isolated/Shared Bridge Evidence Detail

This is a read-only audit of the previous R3R10 and R3R11 reports. It extracts the actual nested `observed` payload and source/goal/step evidence without inventing typed proof identities. It inventories source guards and records why a provider-level diagnosis remains unconfirmed. No production code or existing test is changed.

Run from the repository root after extracting the ZIP:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase176_R3R12_Bridge_Evidence_Detail.zip" -DestinationPath "." -Force
$script = ".\phase176_r3r12_bridge_evidence_detail\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R12 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R12 audit failed" }
git diff --check
git diff --stat
git status -sb
```

The focused tests use `-p no:cacheprovider` to prevent further modifications to pytest's tracked cache. The full suite is intentionally not run. A success gate indicates evidence extraction, **not** a proven bridge or a completed group proof. The JSON report is written under `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r12_bridge_evidence_detail\report.json`.
