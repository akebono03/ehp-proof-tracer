# Phase 155 Closure-R2C-R4 overlap / redundancy audit

## Boundary

- KEEP_ROUTINE_CANDIDATE reviewed: 14
- Repository test bodies executed: 0
- Repository files changed: 0
- Production changes: none

## Classification

```text
KEEP: 3
MERGE_CANDIDATE: 5
DELETE_CANDIDATE: 6
```

## Overlap groups

```text
phase153_all_group_reference_population: 3
phase153_pi10_6_reference_baseline: 3
rendered_source_metadata: 2
representative_provenance_matrix: 3
result_goal_source_distinction: 2
source_metadata_provenance: 1
```

## Review table

| classification | overlap group | asserts | nodeid |
| --- | --- | ---: | --- |
| DELETE_CANDIDATE | phase153_pi10_6_reference_baseline | 3 | `tests/test_phase153_r2_public_reference_semantic_fact.py::test_phase153_r2_public_pi10_6_excludes_obsolete_45_reference` |
| MERGE_CANDIDATE | phase153_all_group_reference_population | 2 | `tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_selected_statements_are_publicly_visible` |
| MERGE_CANDIDATE | phase153_all_group_reference_population | 2 | `tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_public_reference_markers_cover_structured_entries` |
| KEEP | phase153_pi10_6_reference_baseline | 3 | `tests/test_phase153_r3_4_reference_statement_rendering_connection.py::test_phase153_r3_4_public_pi10_6_reference_section_excludes_obsolete_45` |
| DELETE_CANDIDATE | phase153_pi10_6_reference_baseline | 3 | `tests/test_phase153_r3_5_reference_body_duplicate_suppression.py::test_phase153_r3_5_public_pi10_6_keeps_current_reference_baseline_without_obsolete_45` |
| MERGE_CANDIDATE | phase153_all_group_reference_population | 1 | `tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement` |
| DELETE_CANDIDATE | source_metadata_provenance | 4 | `tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_integrates_calculation_source_metadata` |
| DELETE_CANDIDATE | result_goal_source_distinction | 2 | `tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_result_source_and_goal_source_remain_distinct` |
| KEEP | rendered_source_metadata | 3 | `tests/test_phase96_full_proof_report_renderer.py::test_phase96_11_actual_pi9_5_full_report_contains_source_metadata` |
| KEEP | rendered_source_metadata | 11 | `tests/test_phase96_human_readable_renderer.py::test_phase96_9_actual_pi9_5_markdown_contains_result_source_and_ehp` |
| DELETE_CANDIDATE | result_goal_source_distinction | 1 | `tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_all_representative_results_keep_result_and_goal_sources_distinct` |
| MERGE_CANDIDATE | representative_provenance_matrix | 3 | `tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_representative_goal_sources_preserve_theorem_phase_and_branch` |
| MERGE_CANDIDATE | representative_provenance_matrix | 4 | `tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_top_level_api` |
| DELETE_CANDIDATE | representative_provenance_matrix | 4 | `tests/test_phase98_representative_convenience_validation.py::test_phase98_6_shortest_path_preserves_goal_source_provenance` |

## Per-test rationale

### `tests/test_phase153_r2_public_reference_semantic_fact.py::test_phase153_r2_public_pi10_6_excludes_obsolete_45_reference`

- classification: `DELETE_CANDIDATE`
- overlap group: `phase153_pi10_6_reference_baseline`
- source assert count: 3
- static signals: standard-report
- rationale: The same pi10^6 public Reference baseline is checked again by Phase153 R3-4 and R3-5. R2 is an older integration checkpoint.

### `tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_selected_statements_are_publicly_visible`

- classification: `MERGE_CANDIDATE`
- overlap group: `phase153_all_group_reference_population`
- source assert count: 2
- static signals: standard-report, render-surface, all-group-population
- rationale: This performs the same 112-group traversal as the marker-coverage and selected-statement audits. Keep the visibility invariant, but merge it into one population audit.

### `tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_public_reference_markers_cover_structured_entries`

- classification: `MERGE_CANDIDATE`
- overlap group: `phase153_all_group_reference_population`
- source assert count: 2
- static signals: standard-report, render-surface, all-group-population
- rationale: This shares the same 112-group build/replay/render traversal with the selected-statement visibility audit. The marker invariant is distinct but should share one audit pass.

### `tests/test_phase153_r3_4_reference_statement_rendering_connection.py::test_phase153_r3_4_public_pi10_6_reference_section_excludes_obsolete_45`

- classification: `KEEP`
- overlap group: `phase153_pi10_6_reference_baseline`
- source assert count: 3
- static signals: standard-report, render-surface
- rationale: This is the focused current public-rendering contract for pi10^6 after structured Reference statement connection.

### `tests/test_phase153_r3_5_reference_body_duplicate_suppression.py::test_phase153_r3_5_public_pi10_6_keeps_current_reference_baseline_without_obsolete_45`

- classification: `DELETE_CANDIDATE`
- overlap group: `phase153_pi10_6_reference_baseline`
- source assert count: 3
- static signals: standard-report
- rationale: The file already has focused suppression-unit tests, while this integration assertion repeats the same pi10^6 Reference baseline retained in R3-4.

### `tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement`

- classification: `MERGE_CANDIDATE`
- overlap group: `phase153_all_group_reference_population`
- source assert count: 1
- static signals: standard-report, all-group-population
- rationale: The structured selected-statement invariant is useful, but it repeats the same 112-group traversal used by R3-10. Merge it into the single Reference population audit.

### `tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_integrates_calculation_source_metadata`

- classification: `DELETE_CANDIDATE`
- overlap group: `source_metadata_provenance`
- source assert count: 4
- static signals: phase95-heavy-fixture
- rationale: R2C-R3 now has a lightweight direct source-presentation metadata contract. Rebuilding the actual pi9^5 end-to-end fixture for the same metadata adds no layer-specific assertion.

### `tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_result_source_and_goal_source_remain_distinct`

- classification: `DELETE_CANDIDATE`
- overlap group: `result_goal_source_distinction`
- source assert count: 2
- static signals: phase95-heavy-fixture
- rationale: R2C-R3 now checks result-source/goal-source distinction directly with a lightweight source-presentation test.

### `tests/test_phase96_full_proof_report_renderer.py::test_phase96_11_actual_pi9_5_full_report_contains_source_metadata`

- classification: `KEEP`
- overlap group: `rendered_source_metadata`
- source assert count: 3
- static signals: phase95-heavy-fixture, render-surface
- rationale: This protects the final full-report text surface. Lower-level provenance tests cannot replace a renderer-output contract.

### `tests/test_phase96_human_readable_renderer.py::test_phase96_9_actual_pi9_5_markdown_contains_result_source_and_ehp`

- classification: `KEEP`
- overlap group: `rendered_source_metadata`
- source assert count: 11
- static signals: phase95-heavy-fixture, render-surface
- rationale: This protects the human-readable Markdown surface, including source/EHP presentation. It is a distinct renderer boundary.

### `tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_all_representative_results_keep_result_and_goal_sources_distinct`

- classification: `DELETE_CANDIDATE`
- overlap group: `result_goal_source_distinction`
- source assert count: 1
- static signals: phase95-heavy-fixture
- rationale: The result/goal-source distinction is now covered directly by the lightweight Phase96 contract; repeating it across six heavy representative fixtures is redundant.

### `tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_representative_goal_sources_preserve_theorem_phase_and_branch`

- classification: `MERGE_CANDIDATE`
- overlap group: `representative_provenance_matrix`
- source assert count: 3
- static signals: phase95-heavy-fixture
- rationale: The six-target provenance matrix overlaps the Phase97 top-level provenance matrix. One representative cross-layer integration audit is sufficient after lightweight source contracts were added.

### `tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_top_level_api`

- classification: `MERGE_CANDIDATE`
- overlap group: `representative_provenance_matrix`
- source assert count: 4
- static signals: phase95-heavy-fixture
- rationale: This is valuable cross-layer coverage, but it overlaps the Phase96 six-target provenance matrix. Preserve one merged representative integration audit rather than both.

### `tests/test_phase98_representative_convenience_validation.py::test_phase98_6_shortest_path_preserves_goal_source_provenance`

- classification: `DELETE_CANDIDATE`
- overlap group: `representative_provenance_matrix`
- source assert count: 4
- static signals: phase95-heavy-fixture
- rationale: R2C-R3 now verifies the facade delegates query construction/result identity, while Phase97 verifies report-layer provenance. Rechecking the same six-target provenance through the facade is redundant.

## Recommended R2C-R5 action

1. Keep the three distinct public/rendering contracts unchanged.
2. Merge the three Phase153 population scans into one opt-in population audit so the 112-group traversal is performed once.
3. Merge the Phase96/97 representative provenance matrices into one representative cross-layer integration audit.
4. Delete only the six tests marked DELETE_CANDIDATE after their covering contracts are revalidated.
5. Do not run the repository-wide suite until the Phase155 closure shards are ready.
