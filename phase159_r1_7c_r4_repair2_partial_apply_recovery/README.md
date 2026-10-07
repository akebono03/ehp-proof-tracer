# Phase 159 R1-7c R4 repair2

## Partial-apply recovery

The previous R4 repair1 stopped after several production edits had already been written.

Already applied before the failure:

- `EXACTNESS_TO_MAP_PROPERTY` prose normalization
- `MULTIPLE_RELATION_TO_ORDER` prose normalization
- `FINAL_GROUP_STRUCTURE` prose normalization
- short exact sequence reason normalization
- `_phase159_r1_7c_r4_normalize_proof_body_prose` helper addition

The failure occurred while connecting the helper to
`_phase158_normalize_public_narrative_contract`.

This recovery package preserves those changes and completes only the remaining work.

## Changes

- structurally connects the proof-body normalizer after equation-number normalization,
- updates the three stale test expectations,
- adds the Phase159 focused regression test.

No import changes.

## Verification

- syntax check for the three changed production modules,
- Phase150 focused renderer tests,
- Phase157 public Narrative regression,
- Phase159 R4 focused regression.

Repository-wide pytest is intentionally not run.

## Next boundary

After these tests pass, rerun the R4 cross-group structural audit before closure.
