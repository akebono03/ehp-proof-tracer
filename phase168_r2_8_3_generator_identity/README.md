# Phase 168 R2-8(3) — Registered Generator Identity

This package connects concrete citation matching to the existing `data/HyoujiGen.csv` master metadata. It recognizes ID 2 (eta), ID 3 (nu-prime), and ID 4 (nu) with explicit dimension and composition checks. It accepts equivalent `Suspension` / `IteratedSuspension(exponent=1)` representations but does not use raw text rewriting.

## Files and changes

- Existing file: `phase166_r3t_goal_source_binding/goal_source.py`; the complete `_same_group_structure()` function is replaced. Its full source is shipped as `replacement_function.py`. Existing imports are unchanged.
- New file: `phase168_r2_8_3_generator_identity/identity.py`; all functions are new and are used only by the citation comparator.
- New focused tests: `tests/test_r2_8_3_generator_identity.py`; no existing tests are modified.
- `apply.py` patches by AST boundaries and saves a backup before modification. Re-running the patch is safe.

## Run on Windows

Unzip into the repository root and execute:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase168_r2_8_3_generator_identity\run.ps1"
```

The script patches the single function, runs the package-specific and two preceding package tests, and re-runs the R2-8(1) citation diagnostic. Full pytest is deliberately deferred until Phase 168 concludes.

## Boundary

No general-proposition specialization, proof-rule creation, publication-order changes, group database changes, or renderer changes. A matching group presentation alone does not prove a mathematical theorem; citation eligibility still requires an existing, unique positioned fixed assertion. The two remaining generic claims are expected to stay unresolved in this phase.
