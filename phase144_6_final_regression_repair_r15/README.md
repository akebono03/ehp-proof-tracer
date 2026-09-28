# Phase 144-6 Final Regression Repair R15

## Scope

This repair changes only:

- `toda_group_proof_narrative_argument_multi_renderer.py`

No test source files are changed.

## Production changes

### `_toda_group_proof_narrative_argument_frontier_hidden_step_ids`

Direct-premise prerequisites are protected for every NarrativeArgument role, not only `ESTABLISH_DEFINITION`.

This is a generic dependency rule. It allows a supporting fact required by a direct premise to remain visible before that premise is rendered.

### `render_toda_group_proof_narrative_multi_argument_markdown`

`CALCULATION` blocks are excluded from cross-Argument non-exact dedup ownership.

A calculation block may participate in more than one Argument derivation context. Marking it or its visible steps as globally seen can remove the source steps required to render a later derivation chain and its connector.

Other non-exact blocks retain the R12 step-aware dedup behavior.

## Focused tests

The runner first executes the six tests that remained failing after the previous check, then the two complete directly related test files.

No full test suite is run in this package.
