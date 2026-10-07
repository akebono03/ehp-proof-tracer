# Phase 159 R1-7c R4 repair1

## residual proof-prose normalization

This repair normalizes residual proof-body prose found by the R4 cross-group audit.

## Production files

- `toda_group_proof_narrative_reason_renderer.py`
  - `render_toda_group_proof_narrative_reason_sentence`
- `toda_group_proof_generic_narrative_renderer.py`
  - `_generic_short_exact_sequence_reason_prose`
- `toda_group_proof_narrative_renderer.py`
  - adds `_phase159_r1_7c_r4_normalize_proof_body_prose`
  - updates `_phase158_normalize_public_narrative_contract`

## Test files

Updated:

- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests/test_phase150_rc4_5f_2_final_group_structure_reason.py`
- `tests/test_phase157_r11_reference_reason_punctuation.py`

Added:

- `tests/test_phase159_r1_7c_r4_repair1_residual_proof_prose_normalization.py`

## Import changes

None.

## Scope

This repair does not change Reference rendering. It does not add target-specific handling for pi6_3 or pi8_5.

Repository-wide pytest is intentionally not run.

## Completion criteria

- pi6_3: audited unnecessary `である.` / `を得る.` fragments are removed.
- pi8_5: pure-math `である.` and duplicate `以上より, この完全性と` are removed.
- pi6_3 Reference remains intact.
- pi11_4 R3 Reference component pruning remains intact.
- focused tests pass.

## Next boundary

Re-run the R4 cross-group audit after this repair. Do not begin the next Phase functionality here.
