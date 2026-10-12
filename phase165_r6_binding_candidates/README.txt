Phase 165 R6 — Source/typed candidate inventory (fail-closed)

This install does not edit the registry, ProofSteps, or Web production path.
Source locator equality is only a candidate for manual mathematical review.

Run from repository root:
Expand-Archive -Path "$HOME\Downloads\phase165_r6_binding_candidates.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r6_binding_candidates\run.ps1"

Outputs: phase165_r6_output/report.json and report.md
Focused pytest only. No full test suite.
