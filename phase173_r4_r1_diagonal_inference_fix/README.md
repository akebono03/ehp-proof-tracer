# Phase 173 R4-R1 — Source-bound Diagonal Inference Fix

This package makes one narrowly scoped change to the existing Toda (5.6) backward proposal for the registered group `pi_7^4`.

The preceding audit proved that the original root had four accepted premises but refused the third because `pi_7^7` was accepted as `GIVEN` while the root rule requires `INFERENCE`. The patch **does not relax this rule**. It wraps the diagonal premise in the existing `SourceBoundGoal`, requiring the existing cited Toda (5.1) scalar-specialization rule to infer it from the screened universal source.

## Installation and check

Extract the ZIP in the repository root on a current, synchronized `develop` branch. Invoke `phase173_r4_r1_diagonal_inference_fix/run.ps1 -DryRun`, then `phase173_r4_r1_diagonal_inference_fix/run.ps1`. The installer checks reviewed Git blobs, rejects unknown local target modifications, and backs up the original rule file outside the repository. It then replaces only `phase173_r4_r1_source_bound_56/rule.py`.

The focused tests check the scoped diagonal proof and an isolated, publication-screened proof search using the existing verified Toda Lemma 5.4 source module. The verification script reports `PHASE173_R4_R1_COMPLETE` and `PHASE173_R4_R1_DIAGONAL_INFERENCE_CERTIFIED`. Their value is not assumed in advance.

## Scope

Modified tracked file: `phase173_r4_r1_source_bound_56/rule.py` (imports and `expand_source_bound_toda56` only).

New package: this folder, including a complete replacement payload, guarded installer, focused tests, verification script, and full code listing.

No changes to production registries, proof constructors, source statements, DB goals, or web renderer. No full test suite. Do not treat this package alone as completion of Phase 173 or of the public Web proof.
