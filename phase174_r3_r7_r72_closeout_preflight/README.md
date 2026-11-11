# Phase 174 R72 — Read-only Closeout Preflight

R72 records closeout prerequisites after the successful R71 regression audit. This package does not close Phase 174 and does not mutate production code, the five canonical documents, the Git index, or the proof registry.

The preflight checks the previously generated R71 report (eight completed public cases and citation counts), checks that the audited source code and the prior R71 audit script are unchanged, and rechecks two genuinely incomplete named-generator public cases: `n=4,k=8` and `n=4,k=31`. R70's completion-only projection must leave both partial models untouched.

The five canonical documents are inspected for a Phase 174 final-closeout record. Missing records are reported as pending work, not silently written. The full active pytest suite is reserved for the phase-end final gate, not R72. The 81 passed focused tests are user-reported R71 evidence, not a new R72 run.

## Commands

From the project repository root on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r72_closeout_preflight\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r72_closeout_preflight\run.ps1"
```

The pinned source boundary allows either the original R71 run HEAD (`01c5246a`) or the audit-only merged R71 HEAD (`b6609959`), provided local HEAD and `origin/develop` match. The R71 report must still attest to its original `01c5246a` run. If `origin/develop`, previously reviewed sources, or tracked files have changed beyond that reviewed boundary, review the differences rather than overriding the safety gate. The final output `PASS_R72_FOCUSED_AND_PREFLIGHT` is **not** a Phase 174 closeout result.
