# Phase 150 Performance Repair R1

## Scope

Changed files:

- `audit_phase144_6_r5_39.py`
  - `build_narrative_necessity_inventory()`
  - Build the six target presentations and edge maps once, then reuse them.
- `tests/test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py`
  - Add one module-scoped fixture and reuse the inventory across six assertions.

No Narrative behavior, mathematical classification, production public API,
renderer routing, or project documentation is changed.

The runner executes only the five focused R5-37 through R5-41 test files.
The full regression suite is not run.
