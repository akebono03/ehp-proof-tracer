Phase 155-R3-3C-r1 — verified duplicate removal repair

Reason for repair
-----------------
The first R3-3C stopped while deleting:

`tests/test_phase109_14_decorated_sigma_finite_cyclic_fallback.py::
test_phase109_14_sigma7_stable_specialization_boundary_remains_unsupported`

The current repository contains TWO top-level definitions with that exact
same function name.

R3-3B correctly proved that the pytest test ID was removable, but the first
R3-3C implementation incorrectly required exactly one source-level function
definition for every test ID.

Repair behavior
---------------
1. Locate the newest sibling backup created by the failed R3-3C run.
2. Verify that it contains all 71 affected source files.
3. Restore all affected files from that backup, thereby undoing the partial
   deletion.
4. Preflight every approved function target in memory before writing any new
   source.
5. If one pytest test ID has multiple same-name source definitions, remove
   ALL of those definitions.
6. Parse every staged modified file before applying any change.
7. Create a fresh R3-3C-r1 backup.
8. Apply the already-approved 161 test-ID removals and 5 whole-file removals.
9. Run focused survivor / affected-file / importer verification.

This is transactional with respect to target discovery: missing targets are
detected before the new removal is written.

Boundary
--------
- production changes: none
- approved test IDs removed: 161
- whole test files deleted: 5
- no unrelated helper/import cleanup
- repository-wide pytest: not run
