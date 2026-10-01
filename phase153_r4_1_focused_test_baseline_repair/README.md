# Phase 153-R4.1 — Focused Test Baseline Repair

## Purpose

Phase 153-R4.1 repairs stale Phase 153 focused-test expectations after the R3 Reference-selection changes.

This package changes tests only. Production code is not modified.

## Changed test files

- `tests/test_phase153_r2_public_reference_semantic_fact.py`
- `tests/test_phase153_r3_4_reference_statement_rendering_connection.py`
- `tests/test_phase153_r3_5_reference_body_duplicate_suppression.py`
- `tests/test_phase153_r3_6_unresolved_reference_statement_rendering.py`
- `tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py`

## Current baseline

For `pi_10^6`:

- `Proposition 5.8` remains the relevant Reference.
- the obsolete `(4.5)` Reference must not be restored,
- the proof must still conclude `pi_10^6 = 0`.

Coverage-count baselines after concrete proof-scope recovery:

- R3-6: `37 -> 42`
- R3-9: `31 -> 33`

The semantic-rendering checks themselves are not relaxed.

## Scope boundary

R4.1 does not change production Reference-selection logic.

The next implementation step is R5:

`root exclusion + used external ancestry preference`.
