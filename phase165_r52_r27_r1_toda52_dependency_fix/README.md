# Phase 165 R52-R27-R1: Toda (5.2) existing-definition dependency

This targeted regression fix injects the **already existing** typed eta2 definition proof step from `_build_phase50_result()["premise_steps"]` into the legacy Toda (5.2) inference run. It does not restore any pi3^2-specific inference rule and does not create a new given source.

## Modified symbol

- `toda_upstream_bootstrap.py`: `build_toda_52_composition_isomorphism_step()` (the complete changed function is written to `audit_output/MODIFIED_FUNCTION.md` on install).

## Usage

Extract the ZIP into the repository root and run `phase165_r52_r27_r1_toda52_dependency_fix/run.ps1`. A backup is created before the source edit. The runner executes only local installer checks and `test_phase165_r52_r9_shared_math.py`; it does not run the full test suite.

**Status:** This is a source-shape guarded fix for the observed regression. Repository tests must pass on the user's current installed source before it can be considered complete. If it fails, do not treat it as a successful migration.
