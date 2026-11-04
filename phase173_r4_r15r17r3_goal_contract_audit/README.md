# Phase 173 R15R17-R3: Read-only Goal and Display Contract Audit

This package audits the **typed identity** of unresolved proof goals and compares existing tests against the unified public narrative introduced in R15R17-R1 and refined in R15R17-R2.

It does not change production code, proof results, proof steps, citations, or existing tests. It does not stage, reset, clean, or commit Git changes. Only focused tests are run.

## Requirements

- Repository `akebono03/ehp-proof-tracer`, `develop`, reviewed local and remote HEAD `aa25a9930d36b61e7588d1ef8e5916a766b569e6`.
- R15R17-R1 integrated into the repository and committed before R15R17-R2.
- R15R17-R2 installed locally, including its `installed_state.json`.
- Python and pytest available from PowerShell.

## Run

Extract the ZIP to the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r17r3_goal_contract_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r17r3_goal_contract_audit\run.ps1"
```

The audit outputs `R15R17R3_GOAL_CASE=` JSON lines containing typed goal identities, mathematical-display collisions, and reversed-equation observations. It also outputs `R15R17R3_CONTRACT=` for historical tests that reference old section headings. These are observations, **not instructions to discard or merge mathematical goals**.

Successful completion requires `R15R17R3_RUNTIME_AUDIT=PASS`, `R15R17R3_FOCUSED_PYTEST=PASS`, `R15R17R3_GIT_INDEX_PRESERVED=PASS`, and `R15R17R3_AUDIT_COMPLETE=PASS`.

## R3R1 reviewed-HEAD correction

The original R3 ZIP required HEAD `11fdf0f5`, but R15R17-R2 was subsequently committed as `aa25a993`. The audit is now pinned to that reviewed `develop` revision. The requirement is read-only; local and remote HEAD must both match before real cases are examined. The script prints the observed local and expected HEAD for diagnostics. No proof or renderer code is modified by R3R1.

## R3R2 canonical Reference heading correction

The R3R1 runtime audit stopped after three incomplete cases: it expected the
literal `## 使用する結果` in *every* proof. The existing common Narrative renderer
instead emits `使用する結果` without Markdown heading syntax for completed proofs.
The completed fourth case therefore reported zero matching headings, which was
incorrectly diagnosed as a duplicate Reference section.

R3R2 changes only `audit.py` and adds the focused
`tests/test_reference_heading_contract.py`. The audit now counts the exact
status-specific heading and distinguishes zero, one, and duplicate occurrences.
The production renderer, model, ProofStep, Citation, search result, and prior
historical tests remain untouched. The checked `develop` HEAD remains
`aa25a9930d36b61e7588d1ef8e5916a766b569e6`.

Use the same `run.ps1` after extracting the R3R2 ZIP over the R3 audit folder.
Run `-DryRun` first, then normal execution. The focused tests include six new
heading-contract checks. A full pytest run remains outside Phase 173 R3.
