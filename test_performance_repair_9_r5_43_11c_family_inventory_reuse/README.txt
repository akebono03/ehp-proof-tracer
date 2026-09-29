Test Performance Repair 9
Phase144-6 R5-43-11c family inventory reuse

Changed files
-------------
tests/test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py
tests/test_phase144_6_r5_43_11c_r2_argument_participation_guard.py

Changed import sections
-----------------------
Both files add:
  import pytest

Changed helper
--------------
Both files replace _inventory() with:
  _inventory_from_contexts(contexts_by_target)

New module-scoped fixtures
--------------------------
Both files:
  contexts_by_target
    Builds _context(n, k) once for each of the six TARGETS in that module.
  inventory
    Builds the inventory once from those shared contexts.

R5-43-11c definition-group test
-------------------------------
The definition-group connected-output test reuses the same contexts_by_target
fixture for (8, 7) and (9, 7), instead of rebuilding those proof contexts.

Why fixtures are not shared across the two files
-------------------------------------------------
This repair deliberately does not add or modify conftest.py. Cross-module
fixture sharing would broaden the change beyond the two local R5-43-11c test
modules. Each module therefore remains independently executable.

Assertions
----------
No assertion is removed or weakened.

Production code
---------------
No changes.

Audit builders
--------------
No changes.

Focused pytest
--------------
python -m pytest -q tests/test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py tests/test_phase144_6_r5_43_11c_r2_argument_participation_guard.py --durations=20

Completion criteria
-------------------
- 6 tests pass.
- git diff --check passes.
- Production and audit builder code remain unchanged.
- Each module builds six target contexts once.
- Each module builds its inventory once.
- The 11c definition-group test reuses shared contexts.
- Existing non-detached, detached, connected-output, and no-target-specific
  branch assertions remain intact.

Boundary
--------
This closes the planned Repair 1-9 performance-cleanup set. It does not
change production Narrative behavior or Phase147 Argument-method ownership.
No whole suite is run here.
