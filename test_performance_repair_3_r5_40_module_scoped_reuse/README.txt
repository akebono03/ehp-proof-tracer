Test Performance Repair 3
Phase144-6 R5-40 module-scoped audit data reuse

Changed file
------------
tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py

Changed imports
---------------
Adds:
  import pytest

New test fixture
----------------
placement_inventory
  Module-scoped result of build_placement_inventory().

Changed test functions
----------------------
All seven existing R5-40 test functions use the shared placement inventory.
Their assertions and semantic coverage remain unchanged.

Production code
---------------
No changes.

Audit builders
--------------
No changes.

Focused pytest
--------------
python -m pytest -q tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py --durations=20

Completion criteria
-------------------
- 7 tests pass.
- git diff --check passes.
- Production and audit builder code remain unchanged.
- build_placement_inventory() is constructed once per test module.
- Runtime drops substantially relative to repeated per-test rebuilding.

Boundary
--------
This repair does not change R5-38, R5-39, R5-41, R5-42,
production Narrative behavior, or Phase147 Argument-method ownership.
