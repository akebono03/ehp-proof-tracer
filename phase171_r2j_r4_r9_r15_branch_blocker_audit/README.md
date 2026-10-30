# EHP Proof Tracer — Phase 171 R15 Root-Branch Blocker Audit

This package analyzes the JSON report produced by the Phase 171 R14 audit. It does not modify the proof engine, create an inference rule, add a `GIVEN` premise, reuse a finished proof, or change the Web trust boundary.

## Requirements

- The `develop` branch of `akebono03/ehp-proof-tracer`.
- A checked-out `phase165_r52_r9_shared_math.py` matching the reviewed R11 Git blob.
- An existing `phase171_r2j_r4_r9_r14_root_branch_diagnostic/output/audit.json` from the successful R14 run.
- Python and pytest installed in the project environment.

## Installation and execution

Extract the ZIP into the root directory of the repository. From PowerShell in the repository root, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r15_branch_blocker_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r15_branch_blocker_audit\run.ps1"
```

The script runs six focused tests with the pytest cache disabled, then analyzes the existing R14 report. It writes `output/audit.json` under this package and prints the number of distinct unresolved goals, root-route propagation counts, and leading blocker candidates.

## Interpretation

An origin event is one observed exception raised inside the original recursive resolver. Multiple such events may involve one mathematically identical goal. Candidate observations compare bounded string representations recorded by R14, not mathematical object identity, so the report is diagnostic rather than proof-certified. A missing provider observation is not the same as a provider returning zero expansions.

`NO_EXPANSION` means no candidate expansion was recorded for that goal during the original R14 search. `PROPOSALS_UNPROVED` means at least one candidate expansion was present but the original resolver reported no verified derivation. `NOT_OBSERVED` means the report cannot determine which category applies. R15 makes no causal claim about why the root failed and does not certify Web completion.

The full source of all new files, including tests, is provided in `CODE_FULL_JA.md`; the audit design is documented in `監査仕様.md`.
