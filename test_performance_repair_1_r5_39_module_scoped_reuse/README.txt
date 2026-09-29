Test Performance Repair 1
Phase144-6 R5-39 module-scoped audit data reuse

Changed file
------------
tests/test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py

Changed test helpers
--------------------
- narrative_necessity_rows
  New pytest fixture, scope="module".
- explanatory_contribution_groups
  New pytest fixture, scope="module".

Changed test functions
----------------------
All eight existing R5-39 test functions receive the shared immutable audit
results instead of rebuilding them independently.

Imports
-------
Adds:
  import pytest

Production code
---------------
No changes.

Audit builders
--------------
No changes.

Why this is safe
----------------
The tests keep the same assertions and still independently construct both
Phase39 narrative-necessity rows and Phase38 explanatory-contribution groups.
Only repeated construction inside the same test module is removed.

Focused pytest
--------------
python -m pytest -q tests/test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py --durations=20

Completion criteria
-------------------
- 8 tests pass.
- git diff --check passes.
- Production and audit builder code remain unchanged.
- The two expensive datasets are each constructed once per module.
- Runtime drops substantially relative to the previous eight ~110-123 second
  calls.

Boundary
--------
This repair does not change R5-38, R5-40, R5-41, R5-42, production Narrative
behavior, or Phase147 Argument-method ownership.
