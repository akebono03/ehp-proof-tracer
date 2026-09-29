Test Performance Repair 7
Phase144-6 R5-43-7 hidden-bridge inventory / semantic module-scoped reuse

Changed file
------------
tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py

Changed import section
----------------------
Adds:
  import pytest

New module-scoped fixtures
--------------------------
hidden_bridge_inventory
  Calls build_hidden_bridge_inventory() once per module.

semantic_by_signature
  Calls _semantic_by_signature() once per module.

Changed tests
-------------
The first two R5-43-7 tests consume the shared fixtures instead of rebuilding
the six-group audit inventory and six-group semantic signature map.

Determinism preservation
------------------------
test_phase144_6_r5_43_7_builder_returns_deterministic_presentation_order
is intentionally not converted to cached semantic results. It still builds
hidden-bridge semantics twice for each presentation and compares proof_step
object identity and presentation order, preserving the original determinism
assertion.

Production code
---------------
No changes.

Audit builders
--------------
No changes.

Focused pytest
--------------
python -m pytest -q tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py --durations=20

Completion criteria
-------------------
- 5 tests pass.
- git diff --check passes.
- Production and audit builder code remain unchanged.
- Audit inventory is built once per module.
- Semantic signature map is built once per module.
- Determinism test retains two builder invocations per presentation.
- Existing semantic-role and public-route assertions remain intact.

Boundary
--------
This repair does not change R5-38 through R5-42, other R5-43 tests,
production Narrative behavior, or Phase147 Argument-method ownership.
