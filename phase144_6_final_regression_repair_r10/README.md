# Phase 144-6 Final Regression Repair R10

## Changed production file

- `toda_group_proof_narrative_argument_multi_renderer.py`
  - import: `is_toda_group_proof_aggregate_statement`
  - `_toda_group_proof_narrative_argument_frontier_hidden_step_ids`
  - `render_toda_group_proof_narrative_multi_argument_markdown`

## Changed tests

- `tests/test_phase143_17_argument_discourse.py`
- `tests/test_phase143_46_multi_argument_narrative_assembler.py`
- `tests/test_phase143_47_multi_argument_shared_contribution_dedup.py`
- `tests/test_phase143_53a_r_aggregate_derivation.py`

## Production repair

1. Empty `arguments` now returns an empty Narrative immediately.
2. Existing generic exactness method evidence is merged back into the local
   argument body when newer argument boundaries exclude it.
3. Aggregate mathematical statements are not hidden merely because they sit
   behind the frontier filter. This preserves general derivation facts such as
   short exact sequences, group order, and injectivity statements.

There is no `pi_15^8` or `pi_16^9` special-case branch.

## Stale test repair

`pi_16^9` now has three NarrativeArguments because the `sigma'''` definition
is represented explicitly. Tests that encoded the historical two-argument
population are updated to the current semantic discourse:

- `sigma'''`: first definition
- `sigma_9`: middle definition
- target group structure: final

The aggregate-definition transition test now expects both definition
transitions and verifies their semantic SUPPORT role.

## Test boundary

The runner executes only the focused failures and their directly related Phase
143 files. It intentionally does not run the full suite.
