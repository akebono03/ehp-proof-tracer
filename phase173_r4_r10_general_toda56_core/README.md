# Phase 173 R4-R10: General Typed Toda (5.6) Inference Core

This package adds a separate, non-public, source-first inference kernel for the fixed Hopf-invariant sphere dimension **n = 4**. Unlike the existing bounded rule, its input check does not use an enumerated list of target dimensions. Typed generator-image checks and prior database ordering still fail closed.

The zero-group case is supported when both earlier typed groups are independently admitted database priors. Unknown generator families, including the presently unproved epsilon-suspension identification for the pi_12^4 target, are rejected.

This step **does not modify production modules**, connect a new public search path, register sources, project a Web narrative, or certify pi_11^4 as complete. It creates an isolated candidate inference rule for subsequent source screening and public integration. The existing pi_7^4 through pi_10^4 published proofs are not modified.

## Changed files and complete source

New directory `phase173_r4_r10_general_toda56_core/` only:

- `core.py`: complete implementations of `checked_general_inputs`, `general_toda56_rule`, and `expand_general_toda56`.
- `verify.py`: source-hash and HEAD preflight plus typed frontier report.
- `run.ps1`: DryRun and focused-test runner.
- `tests/test_core.py`: complete focused tests.
- `README.md`, `監査計画.md`, `__init__.py`: scope, instructions, and package marker.

No existing import block, class, method, or function is replaced.

## Windows commands

Expand `EHP_Phase173_R4_R10_GENERAL_TODA56_CORE.zip` at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r10_general_toda56_core\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r10_general_toda56_core\run.ps1'
```

The runner requires branch `develop`, HEAD `7158a7f544cd7c6750ebdf82a3b946caa980ea04`, identical GitHub remote HEAD, and exact reviewed source blobs. Existing tracked edits cause the runner to stop without touching them. Existing untracked folders are preserved.

Focused pytest covers this kernel plus the previously verified bounded source-first and Web regression suites. The complete suite remains reserved for Phase 173 closeout.
