# Phase 176 R3R37 — Public Composite-Right Hopf Hook

This patch connects the previously isolated, source-dependent R3R36 composite-right Hopf rule to the existing shared backward proof search. It does not create a theorem, citation, direct GIVEN, completed group proof, or new mathematical rule. R3R31 and R3R35 are preserved.

## Prerequisites

Run from the repository root on the `develop` branch. The existing R3R30, R3R34, R3R35, and R3R36 source modules must be present. The installer rejects uncommitted changes in `phase165_r52_r9_shared_math.py` rather than overwriting them. It also rejects missing, duplicate, moved, or partially applied code anchors.

The installer modifies only `shared_expansion_provider()` in `phase165_r52_r9_shared_math.py` by inserting one additive provider invocation inside its nested `expand()`. No top-level imports or existing APIs change.

## Execution

From the repository root in Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r37_composite_right_hopf_public\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r37_composite_right_hopf_public\run.ps1
```

DryRun validates the checkout and emits the entire proposed replacement function without changing the production file. Normal execution installs the five-line additive hook (idempotently), runs a source-screened public candidate audit and only focused pytest invocations.

## Outputs

The local reports, an exact pre-change backup, and `CHANGED_FUNCTION_FULL_JA.md` (the full updated `shared_expansion_provider()` including its nested `expand()`) are written to:

`%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r37_composite_right_hopf_public\`

The public audit independently checks: one cited formula candidate; one substitution candidate; two independently provable subgoals; a local inference replay from screened source GIVEN steps; and preservation of both the R3R35 composite-suspension and legacy single-factor paths.

**Limit:** A local replay of independently screened GIVEN steps is not a verification that the shared DFS source-order/citation gate closes the target. The final Hopf image and the group structure remain unproved by this patch. No full pytest run is performed.
