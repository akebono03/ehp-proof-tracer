# Phase 150 R5-43-10 Fixture Performance Repair

## Changed file

`tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py`

## Changed functions / fixtures

- `_data_from_context` is replaced by:
  - `_ordered_from_context`
  - `_connected_from_context`
- `data_by_target` is replaced by:
  - `ordered_by_target`
  - `pi6_connected`
- The three tests that previously consumed `data_by_target` are updated in full
  to consume only the data they actually assert.

## Rationale

The Fixture Breakdown Audit measured about 53.92 seconds for the old
six-target `data_by_target` construction. Of that, 24.46 seconds were spent
building `connected` output for all six targets.

Only the two pi_6^3 string-placement assertions need connected markdown.
The sixteen-chain count needs ordered contributions for all six targets, but
does not need connected markdown.

This repair therefore keeps all mathematical assertions and public renderer
coverage while avoiding connected rendering for the five targets whose
connected markdown is never inspected.

## Phase boundary

This is test-fixture performance work only. It does not optimize production
renderers, alter Narrative semantics, or begin Phase 151 generic-route work.

The full suite is intentionally not run by this package. Phase 150 will run
the full regression only after focused performance repairs are complete.
