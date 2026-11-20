# EHP Proof Tracer — Phase 176 R3R5

A read-only audit of the source-backed Toda Lemma 5.7 zero-suspension identity and right-composition transport needed for the unfinished `(n,k)=(3,5)` group.

The archive creates **only** `phase176_r3r5_lemma57_right_composition_frontier/`. It does not alter production code, registry assertions, proof search, renderer, or project-wide documents. The observed database presentation remains an unproved candidate until separately admitted or inferred by the existing source-first policy.

## Run from the repository root

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase176_R3R5_Lemma57_Right_Composition_Frontier.zip" -DestinationPath "." -Force
$script = ".\phase176_r3r5_lemma57_right_composition_frontier\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R5 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R5 audit failed" }
```

The normal runner executes focused pytest and a subprocess-based, read-only audit, and writes its report under `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r5_lemma57_right_composition_frontier\report.json`. The full pytest suite is deliberately not run. A PASS means only that the audit collected its evidence, **not** that the target proof is complete.

The complete new source and tests are reproduced in `CODE_FULL_JA.md`. The study plan and proof boundaries are documented in Japanese in `AUDIT_PLAN_JA.md`.
