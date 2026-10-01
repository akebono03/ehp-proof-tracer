# Phase 155-R2 — stale expectation audit

## Boundary

This is a static expectation audit. It does not execute the repository-wide pytest suite, rewrite tests, delete tests, or change production code.

- Repository root: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`
- Git HEAD: `bd2dd02767b5f63736926fd092833b1214b38315`
- Test files scanned: 842
- Expectation findings: 413
- High stale candidates: 83
- Medium stale candidates: 1
- Contract-sensitive review findings: 286
- Current-compatible evidence: 43

## Status counts

| status | findings |
| --- | ---: |
| `stale_candidate_high` | 83 |
| `stale_candidate_medium` | 1 |
| `contract_sensitive_review` | 286 |
| `current_compatible` | 43 |

## Contract counts

| contract | findings |
| --- | ---: |
| `ascii_prose_punctuation` | 91 |
| `fixed_snapshot_risk` | 286 |
| `no_internal_fallback_leakage` | 35 |
| `reference_relevance_and_root_exclusion` | 1 |

## High-candidate files

- `tests/test_phase110_12_operation_query_proof_replay_statement_presentation.py`
- `tests/test_phase111_12_deep_show_proof_safe_fallback.py`
- `tests/test_phase132_6_group_proof_narrative_renderer.py`
- `tests/test_phase143_42_argument_body_contribution_renderer.py`
- `tests/test_phase143_46_multi_argument_narrative_assembler.py`
- `tests/test_phase143_47_multi_argument_shared_contribution_dedup.py`
- `tests/test_phase143_53b_r_conclusion_aware_connector.py`
- `tests/test_phase143_53b_transition_connectors.py`
- `tests/test_phase143_55b_conclusion_step_ordering.py`
- `tests/test_phase143_59b_group_structure_duplicate_suppression.py`
- `tests/test_phase143_61b_direct_premise_narrative.py`
- `tests/test_phase143_61b_r_semantic_suppression_priority.py`
- `tests/test_phase143_63a_r_exactness_repair.py`
- `tests/test_phase143_63a_residual_fallback_provenance.py`
- `tests/test_phase144_5_generic_definition_order_equations.py`
- `tests/test_phase144_6_pi6_generic_production_route.py`
- `tests/test_phase144_6_r25_9a_pi5_suppression.py`
- `tests/test_phase144_6_r25_9a_r1_relocation_hidden.py`
- `tests/test_phase144_6_r4_supporting_fact_filtering.py`
- `tests/test_phase146_7_generic_argument_purpose_prose.py`
- `tests/test_phase148_rc2_4_post_repair_six_group.py`
- `tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py`
- `tests/test_phase150_rc4_7b_production_repair.py`
- `tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py`
- `tests/test_phase153_r10_used_reference_filtering.py`
- `tests/test_phase153_r12_root_reference_exclusion.py`
- `tests/test_phase153_r2_public_reference_semantic_fact.py`
- `tests/test_phase153_r3_11_reference_body_ownership_repair.py`
- `tests/test_phase153_r3_5_reference_body_duplicate_suppression.py`
- `tests/test_phase153_r9_reference_reuse_derivation_suppression.py`
- `tests/test_phase71_probe.py`
- `tests/test_phase73_probe.py`
- `tests/test_phase74_probe.py`
- `tests/test_phase75_probe.py`
- `tests/test_phase78_stable_two_primary_identification.py`
- `tests/test_phase96_final_proof_report_audit.py`
- `tests/test_phase96_full_proof_report_renderer.py`
- `tests/test_phase96_proof_step_mathematical_narrative.py`

## Medium-candidate files

- `tests/test_phase132_8_group_proof_narrative_dedup.py`

## Interpretation

- `stale_candidate_high` means the expected literal directly conflicts with a Phase 154 public presentation contract and should be inspected first.
- `stale_candidate_medium` means an older positive Reference expectation may predate Phase 153 Reference relevance/root-exclusion rules; it is not automatically stale.
- `contract_sensitive_review` marks fixed numeric snapshot/count expectations that are fragile under later structural generalization.
- `current_compatible` records negative expectations that explicitly enforce the current contract; these are evidence to preserve, not removal candidates.

## R2 boundary

R2 only identifies expectation-level candidates. Do not delete or rewrite tests from this report alone. The next step is to inspect high/medium candidates against current production behavior with focused tests, then carry only confirmed stale expectations into R2 repair or R3 consolidation.
