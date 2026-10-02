# GitHub baseline — Phase 155-R2C

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Before implementing R2C, current GitHub test bodies were inspected for the
R2B-confirmed failures, including:

- `tests/test_phase132_6_group_proof_narrative_renderer.py`
- `tests/test_phase143_42_argument_body_contribution_renderer.py`
- `tests/test_phase143_46_multi_argument_narrative_assembler.py`
- `tests/test_phase143_53b_r_conclusion_aware_connector.py`
- `tests/test_phase144_6_pi6_generic_production_route.py`
- `tests/test_phase146_7_generic_argument_purpose_prose.py`
- `tests/test_phase148_rc2_4_post_repair_six_group.py`
- `tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py`
- `tests/test_phase150_rc4_7b_production_repair.py`
- `tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py`
- `tests/test_phase153_r10_used_reference_filtering.py`
- `tests/test_phase153_r2_public_reference_semantic_fact.py`
- `tests/test_phase153_r3_5_reference_body_duplicate_suppression.py`

The R2B execution evidence was used as the repair oracle:
45 failed tests, 16 passed tests, 65 confirmed-stale findings, 0 inconclusive.

R2C changes tests only. It does not change the Narrative renderer, proof graph,
theorem facts, Reference selection implementation, or production API.
