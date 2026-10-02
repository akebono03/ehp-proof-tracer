# Phase 155 Closure-R2 failure classification

## Summary

```text
failed nodeids: 98
SAFE_STALE: 38
HISTORICAL_HEAVY: 36
CONTRACT_SENSITIVE: 24
UNKNOWN: 0
```

## Phase-family breakdown

```text
phase132: 5
phase133: 7
phase143: 21
phase144: 36
phase150: 5
phase153: 7
phase95: 3
phase96: 9
phase97: 3
phase98: 2
```

## Category meaning

- `SAFE_STALE`: historical display/string expectation; eligible for focused stale-expectation repair.
- `HISTORICAL_HEAVY`: old cross-group/population/internal audit; review redundancy and runtime before deciding repair/delete/archive.
- `CONTRACT_SENSITIVE`: Reference ownership/provenance/source metadata/aggregate-result semantics; requires contract diagnosis.
- `UNKNOWN`: no reviewed rule. Closure-R2 must end with zero.

## Category / phase matrix

```text
SAFE_STALE: phase132=5, phase133=7, phase143=21, phase150=5
HISTORICAL_HEAVY: phase144=36
CONTRACT_SENSITIVE: phase153=7, phase95=3, phase96=9, phase97=3, phase98=2
UNKNOWN: 
```

## Slowest failed-test evidence

The full-suite log is used only as measured evidence; Closure-R2 does not rerun these tests.

```text
  508.30s call     tests/test_phase97_single_found_calculation_to_report_api.py::test_phase97_3_aggregate_found_preserves_goal_source_provenance
  281.49s call     tests/test_phase95_top_level_calculation_orchestration.py::test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order
  276.88s call     tests/test_phase97_not_found_multiple_results_top_level_handling.py::test_phase97_4_multiple_aggregate_results_preserve_goal_source_order
   27.64s setup    tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py::test_phase144_6_r5_43_7_reproduces_all_r5_43_6_hidden_bridge_signatures
   25.59s call     tests/test_phase144_6_r5_43_9.py::test_phase144_6_r5_43_9_all_chains_observe_same_operation_kind
   25.53s call     tests/test_phase144_6_r5_43_8.py::test_phase144_6_r5_43_8_finds_sixteen_three_step_transport_chains
   25.41s call     tests/test_phase144_6_r5_43_8.py::test_phase144_6_r5_43_8_has_one_hidden_signature_sequence
   24.74s call     tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_final_completion_invariants_pass
   24.57s call     tests/test_phase144_6_r5_43_9.py::test_phase144_6_r5_43_9_all_three_candidate_prose_levels_are_supported_by_observed_data
   24.52s call     tests/test_phase144_6_r5_43_8.py::test_phase144_6_r5_43_8_reports_all_forty_eight_transport_occurrences
   24.10s call     tests/test_phase144_6_r5_43_6.py::test_phase144_6_r5_43_6_pi6_contains_expected_transport_and_integration_candidates
   13.07s setup    tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_pi6_order_matches_phase41_topological_order
   12.36s setup    tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3
    7.67s call     tests/test_phase153_r3_11_reference_body_ownership_repair.py::test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates
    7.08s call     tests/test_phase143_75p_prop44_suspension_injective_semantic_rendering.py::test_phase143_75p_all_target_occurrences_render_semantically
    6.96s call     tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement
    6.82s call     tests/test_phase133_10_sigma_label_wording.py::test_phase133_10_sigma9_depth_two_uses_final_japanese_wording
    6.79s call     tests/test_phase143_75p_prop44_suspension_injective_semantic_rendering.py::test_phase143_75p_both_rule_families_use_same_semantic_renderer
    6.71s call     tests/test_phase143_75p_prop44_suspension_injective_semantic_rendering.py::test_phase143_75p_concrete_map_uses_source_and_target_groups
    6.68s call     tests/test_phase143_75s_toda58_whitehead_square_semantic_rendering.py::test_phase143_75s_all_aggregate_components_render_semantically
```

## Repair boundary

Closure-R2 does not modify production code and does not rerun the 10,421-test repository suite.

`SAFE_STALE` is the only automatic repair candidate lane.

`HISTORICAL_HEAVY` and `CONTRACT_SENSITIVE` remain unchanged until their own focused review.
