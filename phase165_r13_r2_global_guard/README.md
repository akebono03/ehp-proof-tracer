# Phase 165 R13-R2 — Global proof-route guard

## Scope

Changed file: `phase164_r5_r2_common_replay.py`.

Changed import: the legacy `build_toda_group_result_proof_replay` import is removed (no other top-level imports).

Changed function (complete replacement): `build_phase164_r5_r2_common_replay`.

New targeted tests: `phase165_r13_r2_global_guard/test_phase165_r13_r2_global_guard.py`. No production tests have been removed or weakened.

## Result

All `Group proof` requests (including narrative/outline/trace) now fail closed with `GoalSearchIncompleteError` until the registered, mathematically verified common goal engine is wired. No group-specific legacy replay is run. The `Group query` result calculation is unchanged.

## Compatibility note

Existing tests that explicitly expect legacy `Group proof` success will fail until their success contracts are migrated. Do **not** reactivate the legacy replay to make those tests green. This package intentionally runs only the new targeted tests; the full suite is deferred until phase closure.

## Completion and next phase boundary

Completion: all 19 targeted assertions pass, including three view modes and six representative groups. This does not certify proof generation. Next: connect the typed statement registry and common backward search to the group-proof UI and restore success one mathematically verified proof at a time, starting with $\pi_3^2$.
