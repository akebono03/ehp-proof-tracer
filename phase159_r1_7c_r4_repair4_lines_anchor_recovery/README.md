# Phase 159 R1-7c R4 repair4

## Lines-anchor recovery

Previous repairs failed only while locating the connection point inside
`_phase158_normalize_public_narrative_contract`.

Repair4 uses a simpler and more stable anchor:

- locate `_phase158_normalize_public_narrative_contract`,
- locate its `lines = [` block,
- insert `_phase159_r1_7c_r4_normalize_proof_body_prose(proof_body)`
  immediately before that block.

This corresponds to the point after proof-body normalization and before public
section reconstruction.

It also normalizes the hidden zero-map exactness sentence in
`toda_group_proof_narrative_contribution_renderer.py`.

No import changes.

Repository-wide pytest is intentionally not run.
