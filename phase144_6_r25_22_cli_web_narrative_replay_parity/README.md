# Phase 144-6 R25-22 CLI / Web Generic Narrative Replay Parity

## Purpose

Unify the proof-replay input used by CLI and Web generic Narrative rendering.

R25-19 made depth-specified CLI Narrative rendering use the complete replay API.
The Web route still built Narrative presentation from the explicitly depth-limited
replay. R25-22 removes that route difference.

## Production change

Only `web_group_proof.py` is changed.

- Import `build_complete_toda_group_result_proof_replay`.
- Keep the ordinary depth-limited replay as the source for:
  - conclusion metadata,
  - visible replay steps,
  - `WebGroupProofView.max_depth`,
  - Trace,
  - Outline.
- For Narrative presentation only, build a complete replay and pass that replay
  to `build_toda_group_proof_presentation()`.

No renderer, equation-numbering algorithm, semantic rule, proof graph, or
repository theorem data is changed.

## Expected effect

For `pi_6^3`, Web depth 2 Narrative receives the same complete proof input used
by the CLI Narrative route. Existing generic equation numbering and dependency
references can therefore reach the Web adapter and KaTeX rendering path.

## Phase boundary

This does not improve presentation quality, reduce the number of displayed
equations, deduplicate definitions, or suppress internal derivations. Those
remain later presentation-rule work.

Repository-wide pytest is intentionally not run here.
