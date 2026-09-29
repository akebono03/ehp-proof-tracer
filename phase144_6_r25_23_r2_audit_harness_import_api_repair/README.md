# Phase 144-6 R25-23-R2 Audit Harness Import/API Repair

## Failure cause

The original R25-23 audit package imported a non-existent module:

`toda_group_result_query`

The current repository obtains standard group results through:

`toda_calculation_facade.build_standard_toda_report`

The original audit also used outdated assumptions for semantic-sidecar and block
construction.

## Repair

R25-23-R2 changes only the R25-23 audit harness.

Production changes: none.

The repaired `_data()` follows the repository's existing test construction:

1. `build_standard_toda_report(n=n, k=k)`
2. `report.candidates[0].source_candidate.group_result`
3. `build_complete_toda_group_result_proof_replay(group_result)`
4. `build_toda_group_proof_presentation(replay)`
5. `build_toda_group_proof_narrative_semantic_sidecar(presentation)`
6. `build_toda_group_proof_narrative_blocks(..., semantic_sidecar=sidecar)`
7. `build_toda_group_proof_narrative_arguments(..., semantic_sidecar=sidecar)`

The audit purpose remains unchanged: measure evidence over-selection,
exactness duplication, and equation forward references.

Repository-wide pytest is intentionally not run.
