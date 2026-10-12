# Phase 163 R4-R88 — Source-scope validation

This package cross-checks the nine R86 claim units with R87 semantic-review metadata and checks that key condition phrases actually occur in the recorded Japanese TeX extracts. It explicitly **does not** verify mathematical correctness, prove the statements, check the original published edition, grant proof eligibility, or allocate production Statement IDs.

Run `run.ps1` from the EHP Proof Tracer project root after R86 and R87. It checks both source files against the bundled snapshots, runs nine focused pytest tests and creates `phase163_r4_r88_output/scope_conditions.json` and `report.md`. It does not change existing project modules. The full pytest suite is not run.

New files: `phase163_r4_r88_claim_conditions.py` (functions `load`, `tail_key`, `assess`, `write_outputs`, `main`), `tests/test_phase163_r4_r88_claim_conditions.py` (nine tests), `r86_claim_review_snapshot.json`, `r87_semantic_gate_snapshot.json`, `run.ps1`, and this README. No existing functions, classes, or imports are changed.
