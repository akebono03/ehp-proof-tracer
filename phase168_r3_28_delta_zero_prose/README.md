# Phase 168 R3-28 — Typed Delta-zero prose

This limited patch modifies only the existing `phase168_r3_27_typed_statement_projection.py` module and adds focused regression tests. It displays a typed `TodaDeltaZeroStatement` already present in the Proof Tree, using its typed source and target groups.

No proof facts, citations, search logic, ordering, exactness chain merging, or renderer function are modified. The original R3-27 module's SHA-256 is checked before applying, and the file is backed up. All existing imports and the entire replacement module are included.

The tests verify Delta-zero prose, a π₃² integration example, and the existing focused R3-23 to R3-27 tests. Full-suite tests are deferred to the end of Phase 168. The tests have not been executed in this packaging environment.
