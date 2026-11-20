# Phase 176 R3R18 Root Child Frontier Audit

Read-only inventory of the root inference candidates and their immediate proof obligations for the group query `(n,k)=(3,5)`.

No production code, mathematical rules, or source claims are modified. The audit does not assert that a candidate is proven. It reads the actual repository under the current `develop` branch and fails closed if required source anchors are missing or tracked files are dirty.

From the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase176_R3R18_Root_Child_Frontier_Audit.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase176_r3r18_root_child_frontier\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase176_r3r18_root_child_frontier\run.ps1"
```

The report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r18_root_child_frontier\report.json`. The report records only the root candidate list and its immediate subgoals, including candidate counts and directly screened source counts. It does not run full pytest or modify the root proof status.
