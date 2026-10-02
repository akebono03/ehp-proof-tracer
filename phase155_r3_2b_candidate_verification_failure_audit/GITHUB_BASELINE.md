# GitHub baseline — Phase 155-R3-2B

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before R3-2B:

- `tests/test_phase143_1_generic_proof_order.py`
- `tests/test_phase143_1b_semantic_proof_order.py`
- `toda_group_proof_generic_narrative_renderer.py`
- `toda_group_proof_narrative_semantics.py`

Both failing tests inspect the complete generic-renderer module source and
assert that no forbidden fragment including the raw substring `pi6` appears.

The current generic renderer contains:

`statement.pi6_4_group_relation`

inside rendering of `TodaProp53FiniteDimensionalStatement`, next to
`pi4_2_group_relation`, `pi5_3_group_relation`,
`higher_eta_squared_group_relation`, and `higher_range`.

GitHub search also shows `pi6_4_group_relation` as a field used to construct
the same finite-dimensional statement in `toda_midstream_bootstrap.py` and in
its Proposition 5.3 integration tests.

This source evidence distinguishes a statement-data field from a conditional
renderer branch. R3-2B performs the same distinction mechanically on the
user's current local source before drawing a conclusion.
