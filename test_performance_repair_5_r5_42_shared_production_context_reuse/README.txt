Test Performance Repair 5
Phase144-6 R5-42 shared production/context reuse

Changed file
------------
tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py

Changed imports
---------------
Adds:
  import pytest

Changed helper
--------------
Replaces _production(n, k) with:
  _production_from_context(context)

This makes the context lifetime explicit and lets the tests reuse the exact
same proof objects when production ordering is compared with that context.

New module-scoped fixtures
--------------------------
contexts_by_target
  Builds _context(n, k) once for each of the six TARGETS.

production_by_target
  Derives ordered production contributions from those shared contexts.

production_rows
  Flattens the shared production results once.

placement_inventory
  Builds the independent Phase40 audit comparison once.

topological_order_audit
  Builds the independent Phase41 audit comparison once.

Determinism preservation
------------------------
The nonunique-order test does not merely read the cached production twice.
It invokes _production_from_context() again on the same shared context and
compares proof_step object identities, preserving the original repeatability
check without rebuilding the expensive proof context.

Production code
---------------
No changes.

Audit builders
--------------
No changes.

Focused pytest
--------------
python -m pytest -q tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py --durations=20

Completion criteria
-------------------
- 9 tests pass.
- git diff --check passes.
- Production and audit builder code remain unchanged.
- Six target contexts are created once per module.
- Production rows are derived from those same contexts.
- Independent Phase40/Phase41 comparisons remain.
- Determinism is still checked by a second production build on the same context.
- Runtime drops substantially.

Boundary
--------
This repair does not change R5-38 through R5-41, any R5-43 test,
production Narrative behavior, or Phase147 Argument-method ownership.
