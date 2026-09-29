# Phase 144-6 Final Regression Repair R12

## Production files

- `toda_group_proof_narrative_argument_body_renderer.py`
  - `render_toda_group_proof_narrative_argument_body_markdown`
- `toda_group_proof_narrative_argument_multi_renderer.py`
  - `render_toda_group_proof_narrative_multi_argument_markdown`

## Change

R12 adds ProofStep-level non-EXACTNESS deduplication while preserving the
existing block-level API.

A partially displayed block is no longer treated as if every step in that block
had been consumed. The multi-argument renderer records the visible ProofStep
identities and the body renderer excludes only those previously displayed steps.

A block is added to the legacy block-level seen set only when every step in the
block was visible in that argument.

There are no pi6_3 or pi8_5 special cases.

## Test boundary

The runner executes the nine Narrative regressions that remained after R11 and
then the directly related R10/R11 boundary files. The full suite is intentionally
not run.
