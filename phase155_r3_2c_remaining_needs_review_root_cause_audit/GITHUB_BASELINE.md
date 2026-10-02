# GitHub baseline — Phase 155-R3-2C

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

The two current focused failures were rechecked in:

- `tests/test_phase143_1_generic_proof_order.py`
- `tests/test_phase143_1b_semantic_proof_order.py`

Both still implement a whole-module forbidden-substring check containing
`"pi6"`.

Phase 155-R3-2B already established on the user's current local source that:
- 2 failing tests support stale-expectation classification,
- 3 AST-level `pi6` occurrences exist,
- 0 of those occurrences participate in control flow.

R3-2C does not re-decide that result. It uses the local R3-2/R3-2B CSV
outputs to determine why the six other `needs_review` pairs were not closed.
