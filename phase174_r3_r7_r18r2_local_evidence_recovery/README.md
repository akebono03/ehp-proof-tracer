# Phase 174 R3-R7-R18R2 — Local Evidence Boundary Recovery

This package corrects **only** `validate_prior_r17()` in the R18 audit module. Windows audit reports are stored under each user's `LOCALAPPDATA` profile, so an earlier successful R17 execution in another profile cannot be assumed to have left readable records here.

The corrected audit accepts present, validated R17/R17R1 reports. When a report is absent, the audit rechecks the current proof search, root candidate count, typed Delta surjectivity display, missing proof steps, and isomorphism-cycle dependency by invoking the existing R17 public audit function. An existing malformed report is never bypassed. The absence is explicitly recorded; no older JSON file is forged or copied between user accounts.

## Reviewed source and scope

- Reviewed remote `develop`: `7ecd12f28b5943b105ac6a953be69b44eae4a26e`.
- The original R18 audit and R18R1 mixed-EOL correction must be available in the repository.
- Only the existing `phase174_r3_r7_r18_delta_image_surjectivity/audit.py` is modified.
- No production mathematics, proof step, accepted GIVEN, source registry, search provider, renderer, or project root documentation is changed.
- A clean audited source is patched in two strictly pinned stages (R18R1 and R18R2). Failed full runs restore only modifications made by that run.

## Execution

Extract the ZIP into the EHP Proof Tracer repository root. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r18r2_local_evidence_recovery\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R18R2 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r18r2_local_evidence_recovery\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'R18R2 audit failed' }
Write-Output '(END)'
```

A successful final gate is `PASS_R18_LIVE_R17_BOUNDARY_REVALIDATED_NO_PRIOR_JSON_COPY`. This indicates a validated **unresolved** proof frontier, not a completed proof of `pi_12^7 = 0`.

Focused tests only. Full pytest is deferred until Phase 174 closeout.
