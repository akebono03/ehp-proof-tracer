# Phase 171 R20R1 — Read-Only Post-Patch Route Audit

The R20 patch was applied successfully, but two integration tests failed. This package diagnoses the **actual** independent routes for the cited $\pi_6^5$ end group. It does not edit production code, revert the existing R20 patch, add a mathematical GIVEN, import completed proof trees, or relax the canonical resolver's uniqueness requirement.

The package requires the `develop` branch, the reviewed original shared provider blob, the exact installed R20 patch, and the prior R19 `output/audit.json`.

Run at the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2J_R4_R9_R20R1_POST_PATCH_ROUTE_AUDIT_ONLY.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r20r1_post_patch_route_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r20r1_post_patch_route_audit\run.ps1"
git status -sb
git diff --stat
```

Each original backward proposal for the right-end group is tested independently with the existing canonical resolver. All descendant goals use the unmodified shared provider. An outcome of `proved` is supported by a real ProofStep, and its GIVEN leaves are rechecked against eligible cited sources. The isolated proof is never fed to another proof-search call.

The audit prints `PHASE171_R20R1_*_ROUTE_OUTCOMES` and saves the full observations to `output/audit.json`. The focused test run includes six pure classification tests and two live contract tests. The full test suite is intentionally not executed.

A patch rollback is not automatic. Preserve the R20 patch until the route report has been recorded, then review its exact tracked diff before deciding on a rollback or replacement.
