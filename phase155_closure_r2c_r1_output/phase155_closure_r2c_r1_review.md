# Phase 155 Closure-R2C-R1 CONTRACT_SENSITIVE review

## Boundary

- Reviewed nodeids: 24
- Repository tests executed: 0
- Production changes: none
- Existing test changes: none

## Phase-family counts

```text
PHASE153: 7
PHASE95: 3
PHASE96: 9
PHASE97: 3
PHASE98: 2
```

## Recommendation counts

```text
AUDIT_ONLY: 1
KEEP_ROUTINE_CANDIDATE: 14
LIGHTWEIGHT_REPLACE: 9
```

## Runtime counts

```text
EXTREME_120S_PLUS: 3
MODERATE_5S_PLUS: 2
UNMEASURED_TOP50: 19
```

## Priority

The first repair target is every `EXTREME_120S_PLUS` test. These tests must not be rerun before replacement.

| seconds | family | recommendation | nodeid |
| ---: | --- | --- | --- |
| 508.30 | PHASE97 | LIGHTWEIGHT_REPLACE | `tests/test_phase97_single_found_calculation_to_report_api.py::test_phase97_3_aggregate_found_preserves_goal_source_provenance` |
| 281.49 | PHASE95 | LIGHTWEIGHT_REPLACE | `tests/test_phase95_top_level_calculation_orchestration.py::test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order` |
| 276.88 | PHASE97 | LIGHTWEIGHT_REPLACE | `tests/test_phase97_not_found_multiple_results_top_level_handling.py::test_phase97_4_multiple_aggregate_results_preserve_goal_source_order` |
| 7.67 | PHASE153 | AUDIT_ONLY | `tests/test_phase153_r3_11_reference_body_ownership_repair.py::test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates` |
| 6.96 | PHASE153 | KEEP_ROUTINE_CANDIDATE | `tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement` |

## Per-test review

### `tests/test_phase153_r2_public_reference_semantic_fact.py::test_phase153_r2_public_pi10_6_excludes_obsolete_45_reference`

- family: `PHASE153`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 3
- signals: reference
- rationale: This appears to be a focused current Reference contract rather than a full population scan. Keep unless later redundancy review proves the same assertion is covered elsewhere.

### `tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_selected_statements_are_publicly_visible`

- family: `PHASE153`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 2
- signals: reference
- rationale: This appears to be a focused current Reference contract rather than a full population scan. Keep unless later redundancy review proves the same assertion is covered elsewhere.

### `tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_public_reference_markers_cover_structured_entries`

- family: `PHASE153`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 2
- signals: reference
- rationale: This appears to be a focused current Reference contract rather than a full population scan. Keep unless later redundancy review proves the same assertion is covered elsewhere.

### `tests/test_phase153_r3_11_reference_body_ownership_repair.py::test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates`

- family: `PHASE153`
- runtime: `MODERATE_5S_PLUS`
- recommendation: `AUDIT_ONLY`
- source assert count: 1
- signals: all_group_scan, reference
- rationale: This is a cross-group Reference/Narrative population audit. Keep the population check out of routine regression and retain small focused renderer/selection contracts routinely.

### `tests/test_phase153_r3_4_reference_statement_rendering_connection.py::test_phase153_r3_4_public_pi10_6_reference_section_excludes_obsolete_45`

- family: `PHASE153`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 3
- signals: reference
- rationale: This appears to be a focused current Reference contract rather than a full population scan. Keep unless later redundancy review proves the same assertion is covered elsewhere.

### `tests/test_phase153_r3_5_reference_body_duplicate_suppression.py::test_phase153_r3_5_public_pi10_6_keeps_current_reference_baseline_without_obsolete_45`

- family: `PHASE153`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 3
- signals: reference
- rationale: This appears to be a focused current Reference contract rather than a full population scan. Keep unless later redundancy review proves the same assertion is covered elsewhere.

### `tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement`

- family: `PHASE153`
- runtime: `MODERATE_5S_PLUS`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 1
- signals: reference
- rationale: This appears to be a focused current Reference contract rather than a full population scan. Keep unless later redundancy review proves the same assertion is covered elsewhere.

### `tests/test_phase95_actual_representative_top_level_capability.py::test_phase95_20_pi9_5_preserves_order_two_generator_and_actual_ehp_provenance`

- family: `PHASE95`
- runtime: `UNMEASURED_TOP50`
- recommendation: `LIGHTWEIGHT_REPLACE`
- source assert count: 10
- signals: representative_builder, provenance
- rationale: The asserted contract is identity/order/provenance, while the test constructs a large historical integration fixture. Replace the fixture with the minimal object graph needed by the current API.

### `tests/test_phase95_actual_representative_top_level_capability.py::test_phase95_20_pi10_4_preserves_order_eight_outer_phase73_branch`

- family: `PHASE95`
- runtime: `UNMEASURED_TOP50`
- recommendation: `LIGHTWEIGHT_REPLACE`
- source assert count: 4
- signals: representative_builder, provenance
- rationale: The asserted contract is identity/order/provenance, while the test constructs a large historical integration fixture. Replace the fixture with the minimal object graph needed by the current API.

### `tests/test_phase95_top_level_calculation_orchestration.py::test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order`

- family: `PHASE95`
- runtime: `EXTREME_120S_PLUS`
- recommendation: `LIGHTWEIGHT_REPLACE`
- source assert count: 5
- signals: aggregate_builder, provenance, order
- rationale: The test protects a small contract but takes at least two minutes. Replace heavy integration builders with minimal synthetic repository/candidate objects that preserve the same provenance or order contract.

### `tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_integrates_calculation_source_metadata`

- family: `PHASE96`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 4
- signals: provenance
- rationale: No evidence from runtime/source shape alone justifies deletion or audit-only treatment. Preserve until an assertion-level replacement or overlap is proven.

### `tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_result_source_and_goal_source_remain_distinct`

- family: `PHASE96`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 2
- signals: provenance
- rationale: No evidence from runtime/source shape alone justifies deletion or audit-only treatment. Preserve until an assertion-level replacement or overlap is proven.

### `tests/test_phase96_full_proof_report_renderer.py::test_phase96_11_actual_pi9_5_full_report_contains_source_metadata`

- family: `PHASE96`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 3
- signals: 
- rationale: No evidence from runtime/source shape alone justifies deletion or audit-only treatment. Preserve until an assertion-level replacement or overlap is proven.

### `tests/test_phase96_human_readable_renderer.py::test_phase96_9_actual_pi9_5_markdown_contains_result_source_and_ehp`

- family: `PHASE96`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 11
- signals: 
- rationale: No evidence from runtime/source shape alone justifies deletion or audit-only treatment. Preserve until an assertion-level replacement or overlap is proven.

### `tests/test_phase96_proof_step_source_presentation.py::test_phase96_5_actual_pi9_5_aggregate_goal_source_preserves_theorem_phase_and_branch`

- family: `PHASE96`
- runtime: `UNMEASURED_TOP50`
- recommendation: `LIGHTWEIGHT_REPLACE`
- source assert count: 7
- signals: representative_builder, provenance
- rationale: The asserted contract is identity/order/provenance, while the test constructs a large historical integration fixture. Replace the fixture with the minimal object graph needed by the current API.

### `tests/test_phase96_proof_step_source_presentation.py::test_phase96_5_actual_aggregate_result_source_and_goal_source_remain_distinct`

- family: `PHASE96`
- runtime: `UNMEASURED_TOP50`
- recommendation: `LIGHTWEIGHT_REPLACE`
- source assert count: 3
- signals: representative_builder, provenance
- rationale: The asserted contract is identity/order/provenance, while the test constructs a large historical integration fixture. Replace the fixture with the minimal object graph needed by the current API.

### `tests/test_phase96_proof_step_source_presentation.py::test_phase96_5_actual_internal_dependency_does_not_inherit_aggregate_theorem_metadata`

- family: `PHASE96`
- runtime: `UNMEASURED_TOP50`
- recommendation: `LIGHTWEIGHT_REPLACE`
- source assert count: 2
- signals: representative_builder, provenance
- rationale: The asserted contract is identity/order/provenance, while the test constructs a large historical integration fixture. Replace the fixture with the minimal object graph needed by the current API.

### `tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_representative_goal_sources_preserve_theorem_phase_and_branch`

- family: `PHASE96`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 3
- signals: provenance
- rationale: No evidence from runtime/source shape alone justifies deletion or audit-only treatment. Preserve until an assertion-level replacement or overlap is proven.

### `tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_all_representative_results_keep_result_and_goal_sources_distinct`

- family: `PHASE96`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 1
- signals: provenance
- rationale: No evidence from runtime/source shape alone justifies deletion or audit-only treatment. Preserve until an assertion-level replacement or overlap is proven.

### `tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_top_level_api`

- family: `PHASE97`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 4
- signals: provenance
- rationale: No evidence from runtime/source shape alone justifies deletion or audit-only treatment. Preserve until an assertion-level replacement or overlap is proven.

### `tests/test_phase97_not_found_multiple_results_top_level_handling.py::test_phase97_4_multiple_aggregate_results_preserve_goal_source_order`

- family: `PHASE97`
- runtime: `EXTREME_120S_PLUS`
- recommendation: `LIGHTWEIGHT_REPLACE`
- source assert count: 6
- signals: aggregate_builder, provenance, order
- rationale: The test protects a small contract but takes at least two minutes. Replace heavy integration builders with minimal synthetic repository/candidate objects that preserve the same provenance or order contract.

### `tests/test_phase97_single_found_calculation_to_report_api.py::test_phase97_3_aggregate_found_preserves_goal_source_provenance`

- family: `PHASE97`
- runtime: `EXTREME_120S_PLUS`
- recommendation: `LIGHTWEIGHT_REPLACE`
- source assert count: 5
- signals: representative_builder, provenance, order
- rationale: The test protects a small contract but takes at least two minutes. Replace heavy integration builders with minimal synthetic repository/candidate objects that preserve the same provenance or order contract.

### `tests/test_phase98_actual_use_facade_validation.py::test_phase98_3_facade_preserves_goal_source_provenance`

- family: `PHASE98`
- runtime: `UNMEASURED_TOP50`
- recommendation: `LIGHTWEIGHT_REPLACE`
- source assert count: 4
- signals: representative_builder, provenance
- rationale: The asserted contract is identity/order/provenance, while the test constructs a large historical integration fixture. Replace the fixture with the minimal object graph needed by the current API.

### `tests/test_phase98_representative_convenience_validation.py::test_phase98_6_shortest_path_preserves_goal_source_provenance`

- family: `PHASE98`
- runtime: `UNMEASURED_TOP50`
- recommendation: `KEEP_ROUTINE_CANDIDATE`
- source assert count: 4
- signals: provenance, order
- rationale: No evidence from runtime/source shape alone justifies deletion or audit-only treatment. Preserve until an assertion-level replacement or overlap is proven.

## Next repair boundary

1. Replace the three extreme Phase95/97 tests first with minimal synthetic contracts.
2. Separate Phase153 all-group population scans into audit-only.
3. Review the remaining focused contract tests for overlap only after the extreme tests are removed.
4. Do not run the repository-wide suite during R2C.
