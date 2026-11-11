# EHP Proof Tracer — Phase 175 R2R1 Source Lineage Repair

This **read-only** package analyzes the three incomplete `k=4` proof searches observed during Phase 175 R1: `pi_7^3`, `pi_9^5`, and `pi_10^6`. It does not install mathematical rules, create source `GIVEN` assertions, replay historical proofs, change source files, modify the canonical documents, or report any previously unfinished root as complete.

## Reviewed dependencies

- GitHub repository: `akebono03/ehp-proof-tracer`, branch `develop`.
- Reviewed Phase 174 merge baseline: `4f87fc5722e85f7365250c07e684e959b71ae8bb`.
- All 11 production-source Git blob pins from Phase 175 R1, plus seven source/rule/test pins specific to R2, are verified.
- The actual six-group R1 audit report is required. Its observed result must be three complete, three incomplete, zero operational failures, and precisely the three reported unproved typed goals. The report and checkout must describe the same source lineage.
- Earlier adopted sources are checked against Toda's Chapter V transcription and source-position manifest, not against a fabricated database citation.

## Windows PowerShell

Extract the R2R1 replacement ZIP **at the root of the existing repository**, overwriting only the R2 audit directory, and run:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase175_R2R1_K4_LINEAGE_FIX.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase175_r2_k4_frontier_audit\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R2 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase175_r2_k4_frontier_audit\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'R2 audit failed' }
git status -sb
```

By default, R2 chooses the latest valid, successful R1 report under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r1_k4_audit\`. To choose a specific report, pass `-R1Report 'C:\Users\oomae\AppData\Local\EHPProofTracerAudit\phase175_r1_k4_audit\20261111T074852_297718Z\report.json'` to each invocation. The PowerShell runner executes only **focused** pytest files (the new R2 tests, R1's existing audit contracts, and Phase 174 R34 source contracts) before running the read-only audit. No project-wide pytest is run.

`-DryRun` validates the exact reviewed production source and R1 evidence but does not launch the live source-screening worker. The normal run launches a single isolated Python worker with a default 240-second timeout. The worker checks typed representations of the previously registered Proposition 5.8 and equation (5.10), screens the two source premises for the `pi_10^6=0` goal, and confirms the older **free-cyclic** Delta rules do not accept the finite-cyclic target. The screen results are observations, not fabricated proofs.

## Outputs and interpretation

Reports are written outside the Git repository to `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r2_k4_frontier_audit\<UTC timestamp>\`:

- `report.json`: R1 provenance, original three typed open-goal lists, actual observed source screening, and refusal/error reasons.
- `report.md`: Japanese source-first frontier summary for R3 planning (normal execution only).
- `source_worker.log`: worker stdout/stderr, retained for debugging.

`PASS_R2_SOURCE_FRONTIER_RECORDED` confirms a truthful read-only audit **only**. It does **not** certify completion of `pi_7^3`, `pi_9^5`, or `pi_10^6`, nor does it certify a new finite-cyclic surjectivity rule. A zero `screened_count` is recorded honestly as a further source/provider gap, not silently treated as success in mathematical derivation.

The source claim `pi_9^5 = Z/2{nu_5 eta_8}` and the typed image fact `Delta(iota_11) = nu_5 eta_8` suggest a future finite-cyclic generator-surjectivity inference for `pi_10^6`, subject to existing source-position and exactness checks. They are not new R2 axioms.

## Files

This ZIP adds only the `phase175_r2_k4_frontier_audit/` directory. `AUDIT_PLAN_JA.md` specifies the audit boundaries and follow-up criteria. `CODE_FULL_JA.md` contains the complete new source, launcher, and tests in directly reusable units.

## R2R1 correction: audited HEAD handoff

The observed R2 DryRun refused with `R2_R1_SOURCE_LINEAGE_CHANGED` after R1 had passed all six `k=4` group audits. The R1 audit directory was initially **untracked**, and GitHub `develop` then merged **eight added files in that directory only**. That is an authorized audit-only advancement, not a modification of the mathematical source code.

`verify_provenance()` continues to require the exact original 11 source-blob pins, the Phase 174 reviewed merge baseline, and `develop`. It accepts either identical R1/R2 HEADs or a later **Git descendant** of R1's recorded HEAD. For a descendant it requires **every intervening file change** to be Git status `A` under `phase175_r1_k4_audit/`; modifications, deletions, unrelated additions, divergent history, and malformed Git SHAs are rejected. The actual lineage mode and allowed paths are recorded in `report.json` and printed. No source guard is bypassed, no source is rewritten, and the R1 results are not re-created.

The fix only changes `audit.py::verify_provenance()`, `audit.py::run()` and the focused audit tests; `run.ps1`, the proof engine, and the other R2 source-audit functions remain unchanged. `CODE_FULL_JA.md` contains complete updated import sections and full function/test files. The command runs the **focused** R2, R1, and prior R34 tests; the full suite is reserved for the end of Phase 175. Running the ZIP does **not** independently certify the previously recorded R1 mathematical results.

This package has been syntax-checked and its R1+R2 audit contract tests have passed locally (58 tests, including a real temporary Git ancestry check). The user's Windows source-worker and prior R34 tests must still run to establish the complete R2 gate. On an unexpected HEAD or source drift, stop and review the actual Git history rather than resetting or ignoring the guard.
