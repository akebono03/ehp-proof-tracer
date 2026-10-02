# Phase 155 Closure-R3-R1 changed code

## Repository changes

None.

## External runner change

The malformed `try:` streaming loop in the original generated
`run_phase155_closure_r3.py` is replaced by the complete
`run_phase155_closure_r3_fixed.py` included in this package.

The fixed `_run_shard()`:
- starts pytest for exactly one shard;
- writes output directly to `shard_NN.log`;
- waits with `timeout=600`;
- catches `subprocess.TimeoutExpired`;
- records `PASS`, `FAIL`, or `TIMEOUT`;
- preserves `checkpoint.json` resume semantics.

The existing `phase155_closure_r3_output/shard_plan.json` is reused unchanged.
