# Phase 155 Closure-R2B Historical-heavy review

## Boundary

- Reviewed nodeids: 36
- Repository tests executed: 0
- Production changes: none
- Existing test changes: none

This report separates runtime-lane advice from redundancy advice.
No test is deleted in R2B.

## Runtime summary

```text
HEAVY_10S_PLUS: 10
UNMEASURED_TOP50: 26
MEASURED_TOTAL_SECONDS: 227.53
```

## Execution-lane recommendation

```text
AUDIT_ONLY: 22
ROUTINE_CANDIDATE: 13
SPLIT_OR_CACHE: 1
```

## Redundancy recommendation

```text
OVERLAP_CANDIDATE: 4
SUPERSEDED_CANDIDATE: 9
UNIQUE_OR_REVIEW: 23
```

## Measured slow tests

| seconds | lane | redundancy | nodeid |
| ---: | --- | --- | --- |
| 27.64 | AUDIT_ONLY | UNIQUE_OR_REVIEW | `tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py::test_phase144_6_r5_43_7_reproduces_all_r5_43_6_hidden_bridge_signatures` |
| 25.59 | AUDIT_ONLY | SUPERSEDED_CANDIDATE | `tests/test_phase144_6_r5_43_9.py::test_phase144_6_r5_43_9_all_chains_observe_same_operation_kind` |
| 25.53 | AUDIT_ONLY | SUPERSEDED_CANDIDATE | `tests/test_phase144_6_r5_43_8.py::test_phase144_6_r5_43_8_finds_sixteen_three_step_transport_chains` |
| 25.41 | AUDIT_ONLY | SUPERSEDED_CANDIDATE | `tests/test_phase144_6_r5_43_8.py::test_phase144_6_r5_43_8_has_one_hidden_signature_sequence` |
| 24.74 | AUDIT_ONLY | OVERLAP_CANDIDATE | `tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_final_completion_invariants_pass` |
| 24.57 | AUDIT_ONLY | SUPERSEDED_CANDIDATE | `tests/test_phase144_6_r5_43_9.py::test_phase144_6_r5_43_9_all_three_candidate_prose_levels_are_supported_by_observed_data` |
| 24.52 | AUDIT_ONLY | SUPERSEDED_CANDIDATE | `tests/test_phase144_6_r5_43_8.py::test_phase144_6_r5_43_8_reports_all_forty_eight_transport_occurrences` |
| 24.10 | AUDIT_ONLY | SUPERSEDED_CANDIDATE | `tests/test_phase144_6_r5_43_6.py::test_phase144_6_r5_43_6_pi6_contains_expected_transport_and_integration_candidates` |
| 13.07 | AUDIT_ONLY | UNIQUE_OR_REVIEW | `tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_pi6_order_matches_phase41_topological_order` |
| 12.36 | SPLIT_OR_CACHE | UNIQUE_OR_REVIEW | `tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3` |

## Superseded candidates

- `tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py::test_phase144_6_r5_43_11_all_sixteen_transport_chains_are_connected` → compare against `test_phase144_6_r5_43_11d_final_completion_audit.py`.
- `tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py::test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations` → compare against `test_phase144_6_r5_43_11d_final_completion_audit.py`.
- `tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py::test_phase144_6_r5_43_11_renderer_has_no_rule_name_or_pi6_specific_branch` → compare against `test_phase144_6_r5_43_11d_final_completion_audit.py`.
- `tests/test_phase144_6_r5_43_6.py::test_phase144_6_r5_43_6_pi6_contains_expected_transport_and_integration_candidates` → compare against `test_phase144_6_r5_43_11d_final_completion_audit.py`.
- `tests/test_phase144_6_r5_43_8.py::test_phase144_6_r5_43_8_finds_sixteen_three_step_transport_chains` → compare against `test_phase144_6_r5_43_11d_final_completion_audit.py`.
- `tests/test_phase144_6_r5_43_8.py::test_phase144_6_r5_43_8_has_one_hidden_signature_sequence` → compare against `test_phase144_6_r5_43_11d_final_completion_audit.py`.
- `tests/test_phase144_6_r5_43_8.py::test_phase144_6_r5_43_8_reports_all_forty_eight_transport_occurrences` → compare against `test_phase144_6_r5_43_11d_final_completion_audit.py`.
- `tests/test_phase144_6_r5_43_9.py::test_phase144_6_r5_43_9_all_chains_observe_same_operation_kind` → compare against `test_phase144_6_r5_43_11d_final_completion_audit.py`.
- `tests/test_phase144_6_r5_43_9.py::test_phase144_6_r5_43_9_all_three_candidate_prose_levels_are_supported_by_observed_data` → compare against `test_phase144_6_r5_43_11d_final_completion_audit.py`.

## Recommended R2B follow-up

1. Keep `43_11d final completion` as the closure-level audit source.
2. For earlier 43_6/8/9/11/11a stages, prove whether each unique assertion is already implied by 43_11d/current contract tests.
3. Move genuine historical population scans to audit-only execution.
4. Replace repeated six-group inventory construction with shared module-scoped context or lightweight representative contracts.
5. Do not re-run the 10,421-test suite during this cleanup.
