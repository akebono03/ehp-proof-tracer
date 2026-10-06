# Phase 159 R1-7c R4 repair3

## Structural recovery + exactness prose normalization

The earlier repair1 partially applied production changes and then stopped while
connecting the new proof-body normalizer. Repair2 also stopped before changing
anything because its source-location heuristic was too strict.

Repair3 preserves the already-applied production edits and completes the work
using line-based structural detection with parenthesis-depth tracking.

It also normalizes the remaining kernel/exactness prose emitted by
`toda_group_proof_narrative_contribution_renderer.py`.

## Production files involved

- `toda_group_proof_narrative_reason_renderer.py`
- `toda_group_proof_generic_narrative_renderer.py`
- `toda_group_proof_narrative_renderer.py`
- `toda_group_proof_narrative_contribution_renderer.py`

## Tests updated

- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests/test_phase150_rc4_5f_2_final_group_structure_reason.py`
- `tests/test_phase157_r11_reference_reason_punctuation.py`
- `tests/test_phase157_r20_repair16_proof_order_and_cleanup.py`
- `tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py`

Added:

- `tests/test_phase159_r1_7c_r4_repair3_residual_proof_prose_normalization.py`

## Import changes

None.

## Verification

The runner performs:

1. recovery apply,
2. `py_compile` on all four affected production modules,
3. focused Phase150 renderer tests,
4. focused Phase157 prose/order regressions,
5. Phase159 R4 focused regression,
6. R4 cross-group re-audit.

Repository-wide pytest is intentionally not run.

## Completion criteria

The R4 re-audit should show no residual audited `である.` / `を得る.` defects
for `pi6_3` and `pi8_5`, while preserving the `pi6_3` Reference boundary and
the `pi11_4` R3 pruning behavior.

## Next boundary

Do not add new proof structures or stable-range behavior in this repair.
