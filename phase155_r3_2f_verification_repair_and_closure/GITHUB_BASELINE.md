# GitHub baseline — Phase 155-R3-2F

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected immediately before implementation:

- `tests/test_phase143_1_generic_proof_order.py`
- `tests/test_phase143_1b_semantic_proof_order.py`
- `toda_group_proof_generic_narrative_renderer.py`

Both Phase 143 tests still prohibit the raw substring `"pi6"` across the
entire generic renderer source.

The current renderer legitimately accesses finite-dimensional statement
fields including:

- `statement.pi4_2_group_relation`
- `statement.pi5_3_group_relation`
- `statement.pi6_4_group_relation`
- `statement.higher_eta_squared_group_relation`
- `statement.higher_range`

Phase 155-R3-2B established locally that current AST-level `pi6` occurrences
do not participate in renderer control flow.

Phase 155-R3-2E then established:
- 11 unique affected base tests,
- 62 fresh call instances,
- 62 passed,
- 0 failed,
- 0 blocking base tests.

Therefore R3-2F repairs only the stale whole-module `"pi6"` substring ban and
the verification aggregation logic. Production behavior is unchanged.
