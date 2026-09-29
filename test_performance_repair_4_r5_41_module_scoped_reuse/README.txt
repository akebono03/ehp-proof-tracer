Test Performance Repair 4
Phase144-6 R5-41 module-scoped audit data reuse

Changed file
------------
tests/test_phase144_6_r5_41_contribution_topological_order_determinism_audit.py

Changed imports
---------------
Adds:
  import pytest
  from audit_phase144_6_r5_40 import build_placement_inventory

The former function-local Phase40 import is moved to the import section.

New test fixtures
-----------------
topological_order_audit
  Module-scoped result of build_topological_order_audit().

placement_inventory
  Module-scoped result of build_placement_inventory(), used only for the
  existing Phase40 population comparison.

Changed test functions
----------------------
All seven existing R5-41 test functions use shared immutable audit results.
Assertions and comparison semantics remain unchanged.

Production code
---------------
No changes.

Audit builders
--------------
No changes.

Focused pytest
--------------
python -m pytest -q tests/test_phase144_6_r5_41_contribution_topological_order_determinism_audit.py --durations=20

Completion criteria
-------------------
- 7 tests pass.
- git diff --check passes.
- Production and audit builder code remain unchanged.
- build_topological_order_audit() is constructed once per test module.
- Phase40 comparison inventory is constructed once per test module.
- Runtime drops substantially relative to repeated per-test rebuilding.

Boundary
--------
This repair does not change R5-38, R5-39, R5-40, R5-42,
production Narrative behavior, or Phase147 Argument-method ownership.
