# Phase 171 R2J-R4-R6 — Finite Cardinality of the Middle Group

This read-only package derives the **cardinality**, not a cyclic presentation, of the EHP middle group from an already inferred short exact sequence and two finite cyclic end-group presentations.

For the Phase 171 instance, the prior source component of Toda Proposition 5.6 identifies `pi_5^2` as a group of order two; that component must be a unique citation-screened earlier `GIVEN`. The `pi_6^5` order-two presentation must be an `INFERENCE` already embedded in the Phase 171 R4-R5 proof tree, ultimately derived from Toda Proposition 5.1. The short exact sequence must itself be inferred from verified EHP exactness and map properties.

The generic rule yields `FiniteGroupCardinality(TodaPrimaryGroup(6,3),4)`. It does not establish the order of `nu-prime` or `pi_6^3 = Z/4{nu-prime}`. It introduces no new `GIVEN`, changes no production source, and does not treat a database target as an axiom. Earlier proof results are reused; their proofs are not required to be repeated in the body of a final narrative.

## Files

- `source.py`: complete generic typed cardinality statement, checked consequence, inference rule, and backward-goal expansion.
- `audit.py`: independent cited-source screening and actual proof-tree reconstruction.
- `tests/test_audit.py`: 10 focused tests, including negative cases and an active end-to-end replay.
- `run.ps1`: preflight, focused pytest, and actual read-only audit.
- `CODE_FULL_JA.md`: full new code and test bodies, including imports.
- `監査仕様.md`: Japanese audit specification.

## Windows PowerShell

From the repository root, extract the accompanying ZIP into `.` and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r6_middle_cardinality\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r6_middle_cardinality\run.ps1"
git status -sb
git diff --stat
```

The runner intentionally does not run the full test suite; reserve that for Phase 171 closeout. Existing files, staging, Git history, and production providers are unchanged.
