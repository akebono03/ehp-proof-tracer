# EHP Proof Tracer — Phase 170 R3-R5

This package implements a minimal, guarded extension of the existing Toda (5.2) cyclic transport. Toda's cited theorem is universal for all `i >= 3`, but the original production implementation proposes a backward proof only at `i = 4`.

## Scope

- One production file: `phase168_r2_toda52_transport.py`. A complete replacement is included in `replacement/`.
- Retains the pre-existing `i = 4` inference without changing its function or guard.
- At `i >= 5`, proposes finite-cyclic `pi_i^2` from an **already screened** finite-cyclic `pi_i^3` Relation and the **already screened** Toda (5.2) universal assertion. Both are mandatory proof subgoals. The generator correspondence is checked against concrete typed compositions and existing `HyoujiGen.csv` identity logic.
- Does not make a DB row a GIVEN, does not adopt an uncited source, and does not use target propositions as their own evidence.
- Does not implement zero or direct-sum transport; those require a separate Phase step and tests.

## Running on Windows PowerShell

From the repository root, unzip the supplied ZIP into `.` and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r5_toda52_cyclic_generalization\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r5_toda52_cyclic_generalization\run.ps1"
git status -sb
```

The runner refuses unexpected tracked changes, an unreviewed HEAD, or a modified original source. It accepts exactly two reviewed develop HEADs. It backs up the complete original file outside the repository under `%LOCALAPPDATA%\EHPProofTracerRecovery` before writing. On failure of focused pytest, the active `pi_5^2` search, or the public Web trust-gated narrative, it automatically restores the original file byte for byte. Reports, logs, and the backup are stored outside the repository.

## Focused tests

Offline mock tests are included and passed 10 checks in the package authoring environment. The Windows runner also executes these relevant real-repository suites:

- `phase170_r3_r5_toda52_cyclic_generalization/tests/test_phase170_r3_r5_toda52_cyclic.py`
- `phase168_r2_toda52_transport/tests/test_phase168_r2_toda52_transport.py`
- `tests/test_phase167_r3_generic_resolver.py`

It then requires `pi_5^2` to be genuinely complete and `build_standard_web_group_proof_view(n=2,k=3,mode="narrative",citation_source="model")` to be complete. These active results are not asserted in advance. The full pytest suite must be deferred to phase closeout.

## Git safety and review

This package does not commit changes, change the index, use checkout/reset, or modify tracked documentation. The original and new function bodies and all imports are included without placeholders. No other production module is edited.
