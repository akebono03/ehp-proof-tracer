# Phase 176 R3R39 — Public Equality Transport

This focused patch connects the six **existing** equality-congruence rules to the shared source-screened backward proof search. It introduces no new mathematical inference rule, source assertion, direct group GIVEN, or precomputed proof.

The provider generates a tentative desuspension candidate from the typed right-hand composite. The existing composite-suspension inference must actually prove this candidate; a structurally proposed factor is never treated as proof evidence. The two upstream obligations continue through the existing R3R35 and R3R37 providers.

The six intermediate conclusions are ordinary `GoalExpansion` steps with their original rule factories. Consequently the shared recursive DFS must check each inference and retain the full proof tree.

## Install and run

Unpack the ZIP in the repository root on the `develop` branch. In PowerShell:

```powershell
$script = ".\phase176_r3r39_public_equality_transport\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw 'DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw 'R3R39 failed' }
```

The DryRun is read-only. The full run idempotently updates only `shared_expansion_provider()` in `phase165_r52_r9_shared_math.py`, audits the actual shared DFS under the screened reference context, and runs focused pytest with `--import-mode=importlib`. It does **not** run the entire suite.

After the full run, `SHARED_FUNCTION_FULL_JA.md` contains the complete updated function as a replacement unit, including its original imports within the function.

**Not yet claimed:** the Toda (5.5) quadruple equality, the final Hopf-image goal, or the complete 5-stem group structure.
