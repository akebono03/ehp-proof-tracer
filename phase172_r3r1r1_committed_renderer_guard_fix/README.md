# Phase 172 R3R1R1 — Committed R2 Renderer Guard Correction

This package corrects only the preflight check in the existing read-only Phase 172 R3R1 Hopf audit. The previous guard wrongly required the R2 renderer patch to remain uncommitted. It now accepts either the reviewed uncommitted patch or the reviewed committed patch, and rejects other source states.

The corrected complete `audit.py` is bundled as `corrected_audit_FULL.py`. No production code, proof search, ProofSteps, source registry, citations, or renderer is changed. The installer checks exact reviewed hashes and backs up the audit source outside the repository. If the corrected audit or tests fail, it restores the former audit source.

From the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase172_R3R1R1_COMMITTED_RENDERER_GUARD_FIX.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r3r1r1_committed_renderer_guard_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r3r1r1_committed_renderer_guard_fix\run.ps1" -RunFocusedTests
```

The final command runs six focused guard tests and delegates to the existing R3R1 audit with its three focused pytest groups. Reports are written under `%LOCALAPPDATA%\EHPProofTracerRecovery`. The complete test suite is not run. The next display-reduction step is deliberately out of scope.
