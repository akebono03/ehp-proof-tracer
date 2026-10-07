# Phase 159 R1-7c R4 repair7

## Final group reason and stale prose expectations

This repair follows the successful production changes from repair6.

The remaining focused failure showed two distinct contracts:

1. `FINAL_GROUP_STRUCTURE` still generated the redundant internal text
   `ord(nu')=4=4`.
2. The contribution renderer intentionally removes the trailing standalone
   connector `したがって,` from the visible public reason paragraph.

Repair7 therefore:

- removes the duplicate numeric equality at the reason-renderer source,
- updates the Phase150 visibility test to compare the connector-free visible
  paragraph,
- updates only test files under `tests/` that directly contain the old prose
  strings changed by R4 normalization.

## Production change

`toda_group_proof_narrative_reason_renderer.py`

`render_toda_group_proof_narrative_reason_sentence()`:

- before: `ord(generator)=order_statement.rhs=middle_order`
- after: `ord(generator)=middle_order`

This is valid because `_final_group_structure_reason()` already verifies that
the order premise equals the target group order and that the product of the
two end-group orders equals the same target order.

## Imports

No import changes.

## Verification

The runner executes only focused tests:

- Phase150 short exact / final group reason tests,
- directly affected Phase157 prose tests,
- repair6 regression,
- repair7 regression,
- R4 cross-group audit.

Repository-wide pytest is intentionally not run.
