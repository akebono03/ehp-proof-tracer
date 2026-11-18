# EHP Proof Tracer — Phase 175 R4R6R2 Historical Audit Fix

This patch corrects an incorrect Git HEAD comparison in the read-only Phase 175 R4R6 audit. R4R5R3 recorded a **historical HEAD before its production wiring commit**; R4R6R1 incorrectly required that historical HEAD to equal one of the **later** R4R6 checkout HEADs. The new implementation validates the recorded historical Git lineage and exact source blobs without weakening source-first requirements.

## Scope

Only the R4R6 audit package is replaced: `audit.py`, `tests/test_audit.py`, and the four documentation files. The existing `run.ps1` is included unchanged. Production modules, shared proof search, mathematical inference rules, GIVEN registrations, and prior proof results are untouched.

The audit still verifies Toda Proposition 2.5, equation (5.8), the case `m=4, i=8, j=9`, the order-two sign argument, typed endpoints, and public-provider boundaries. It does **not** construct a ProofStep or complete `pi_9^5`.

## Installation and execution (PowerShell)

Extract `EHP_Phase175_R4R6R2_Historical_Prior_Head_Fix.zip` at the repository root using `Expand-Archive -Force`. Run from the root:

```powershell
$script = '.\phase175_r4r6_prop25_eq58_source_frontier\run.ps1'
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File $script
```

A known successful R4R5R3 report may be passed with `-R4R5R3Report <absolute-path-to-report.json>` to each invocation. The script performs focused pytest before the read-only audit.

## Expected results

A successful DryRun uses `PASS_R4R6_PROP25_EQ58_SOURCE_DRYRUN`. A successful real run uses:

`PASS_R4R6_PROP25_EQ58_SOURCE_FRONTIER_RECORDED_NOT_PUBLIC`

Both runs write reports under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r4r6_prop25_eq58_source_frontier`. The full test suite is intentionally not run until the end of Phase 175.
