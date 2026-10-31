# Phase 172 R3R1 — Read-only Hopf proof display audit

This package audits the completed canonical proof of $\pi_6^3=\mathbb{Z}/4\{\nu'\}$ after the verified Phase 172 R2 suspension-display patch. It does not change existing repository sources, tests, mathematical inferences, references, or proof steps.

Extract the ZIP into the root of the `ehp-proof-tracer` working tree on `develop`. The R2 and R2R1 packages must already be installed, and the 9-line renderer patch must still be present.

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase172_R3R1_HOPF_CHAIN_AUDIT_ONLY.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r3r1_hopf_chain_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r3r1_hopf_chain_audit\run.ps1" -RunFocusedTests
git status -sb
git diff --stat
```

The runner first checks local `develop`, the reviewed committed renderer Git blob, the exact R2 renderer transformation, and R2R1-corrected source and test hashes. When reachable, `origin/develop` must match local HEAD. It then runs one real canonical backward proof search, verifies the existing trust boundary, and audits the proof-step ancestry of the Hopf-image equality used by an inferred surjectivity step.

Reports are saved outside the working tree to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r3r1_<UTC timestamp>\`. Outputs: `audit.json`, `hopf_steps.json`, `hopf_display_alignment.json`, `reference_provenance.json`, `web_narrative.md`, `AUDIT_FINDINGS_JA.md`, and focused pytest logs.

All textual matches are diagnostic candidates, not deductions. No full pytest run occurs; save that for Phase 172 closeout. R3 presentation changes are explicitly out of scope.
