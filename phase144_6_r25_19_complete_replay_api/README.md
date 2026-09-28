# Phase 144-6 R25-19 Complete Replay API

## Production changes

### `toda_group_result_proof_replay.py`

Add:

`build_complete_toda_group_result_proof_replay(group_result)`

The existing `build_toda_group_result_proof_replay(group_result, max_depth=1)`
API is unchanged.

The complete builder obtains the actual maximum `shortest_depth` from the
recursive proof provenance and delegates to the existing bounded replay
builder. No fixed large depth is used.

### `main.py`

`_run_group_proof_command()` keeps bounded replay for Trace and Outline.

When Narrative is requested with an explicit depth, its presentation uses the
new complete replay API so that the mathematical Narrative is not truncated
mid-derivation.

## Focused tests

- complete replay reaches the real leaf depth
- existing default depth remains 1
- invalid input contract
- existing Phase 131 replay tests
- pi_6^3 CLI Narrative definition and equation connectors
- no raw rule-name fallback
- R25-9B depth=2 semantic-closure contract
- generic pi_6^3 production route

No full pytest is run in this package.
