Test Performance Repair 8
Phase144-6 R5-43-10 six-group data / hidden-bridge semantics reuse

Changed file
------------
tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py

Changed import section
----------------------
Adds:
  import pytest

Changed helper
--------------
Replaces:
  _data(n, k)

with:
  _data_from_context(context)

The production-data helper now consumes an already-built proof context.

New module-scoped fixtures
--------------------------
contexts_by_target
  Builds _context(n, k) once for each of the six TARGETS.

hidden_bridge_semantics_by_target
  Derives hidden-bridge semantics once per target from the shared presentation.

data_by_target
  Derives presentation / ordered contributions / connected Narrative once per
  target from the same shared context.

Changed tests
-------------
The two hidden-bridge semantic tests reuse hidden_bridge_semantics_by_target.
The three connector/compression behavioral tests reuse data_by_target.
The two source-inspection tests remain independent.

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
python -m pytest -q tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py --durations=20

Completion criteria
-------------------
- 7 tests pass.
- git diff --check passes.
- Production and audit builder code remain unchanged.
- Six target contexts are built once per module.
- Hidden-bridge semantics are derived once per target.
- Narrative/ordered/connected data are derived once per target.
- Existing metadata, transport-triplet, connector, compression, and
  no-target-specific-branch assertions remain intact.

Boundary
--------
This repair does not change R5-38 through R5-42, other R5-43 tests,
production Narrative behavior, or Phase147 Argument-method ownership.
