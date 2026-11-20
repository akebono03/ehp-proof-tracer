# Phase 176 R3R14: Isolated Two-Stage Backward Provider

This read-only audit composes two existing, independently tested inference boundaries without modifying the production EHP Proof Tracer. A screened citation of Toda Lemma 5.7 may justify the base zero-suspension statement. A separate, typed right-composition transport rule may then derive a longer zero-suspension statement. Both obligations remain independent in the proof tree.

## Requirements

- Run from the `develop` branch of `akebono03/ehp-proof-tracer`.
- The reviewed commit `51855066237e710c6715250478f9a731bc1c087f` must be an ancestor of the current HEAD.
- The preceding Phase 176 code and Toda source must be present.
- Tracked repository files must be clean.

## Execute

Extract the ZIP into the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase176_r3r14_isolated_two_stage_provider\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase176_r3r14_isolated_two_stage_provider\run.ps1"
```

The report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r14_isolated_two_stage_provider\report.json`.

## Scope and limitations

This package adds only an isolated provider, its audit, focused tests, and documentation. It does not register anything in `shared_expansion_provider`, add a new GIVEN, modify the public renderer, or declare the target group complete. The live audit reconstructs two nested inference steps from screened sources. Full-suite pytest is deferred until the end of the Phase.
