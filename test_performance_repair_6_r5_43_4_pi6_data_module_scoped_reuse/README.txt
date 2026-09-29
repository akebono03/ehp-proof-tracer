Test Performance Repair 6
Phase144-6 R5-43-4 _pi6_data() module-scoped reuse

Changed file
------------
tests/test_phase144_6_r5_43_4_dependency_aware_contribution_connector.py

Changed import section
----------------------
Adds:
  import pytest

Existing imports remain unchanged.

New fixture
-----------
pi6_data
  Module-scoped fixture returning _pi6_data() once.

Changed test functions
----------------------
The five behavioral R5-43-4 tests now accept pi6_data and unpack the
shared tuple instead of rebuilding _pi6_data() independently.

The source-inspection test remains independent and unchanged in behavior.

Assertions
----------
No assertion is weakened or removed.

Production code
---------------
No changes.

Audit builders
--------------
No changes.

Focused pytest
--------------
python -m pytest -q tests/test_phase144_6_r5_43_4_dependency_aware_contribution_connector.py --durations=20

Completion criteria
-------------------
- 6 tests pass.
- git diff --check passes.
- Production and audit builder code remain unchanged.
- _pi6_data() is constructed once per module.
- Existing connector, placement, ordering, uniqueness, and no-target-branch
  assertions remain intact.
- Runtime drops substantially.

Boundary
--------
This repair does not change R5-38 through R5-42, other R5-43 tests,
production Narrative behavior, or Phase147 Argument-method ownership.
