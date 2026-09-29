Test Performance Repair 2
Phase144-6 R5-38 module-scoped audit data reuse

Changed file
------------
tests/test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py

Changed imports
---------------
Adds:
  import pytest

New test fixtures
-----------------
- visibility_occurrences
  Module-scoped result of build_visibility_occurrences().
- explanatory_contribution_groups
  Module-scoped result of build_explanatory_contribution_groups().
- semantic_equivalence_and_rendering_inventory
  Module-scoped Phase37 comparison inventory.

Changed test functions
----------------------
All six existing R5-38 test functions use shared immutable audit results.
Their assertions and comparison relationships remain unchanged.

Production code
---------------
No changes.

Audit builders
--------------
No changes.

Focused pytest
--------------
python -m pytest -q tests/test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py --durations=20

Completion criteria
-------------------
- 6 tests pass.
- git diff --check passes.
- Production and audit builder code remain unchanged.
- Each expensive dataset is constructed once per test module.
- Runtime drops substantially relative to repeated per-test rebuilding.

Boundary
--------
This repair does not change Repair 1 / R5-39, R5-40, R5-41, R5-42,
production Narrative behavior, or Phase147 Argument-method ownership.
