Phase 159 repair2g fix10e

Purpose
-------
Retry fix10d with an exact line-based patcher.

fix10d failed before changing production code because the apply script's
marker string for generic_used_step_ids contained the wrong newline
escaping.

fix10e does not search for escaped newline-containing blocks.

Changed file
------------
toda_group_proof_narrative_contribution_renderer.py

New helper
----------
normalize_toda_group_proof_narrative_numbered_map_property_display()

Insertion position
------------------
Immediately before:
render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

Changed function
----------------
render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

The normalization call is inserted immediately before the exact source
line:

  generic_used_step_ids = (

Generic normalization
---------------------
- numbered 単射 / 全射 / 同型 map-property lines are converted from
  inline \tag{N} form to display-math ... \qquad (N) form.
- は零写像である. is normalized to は零写像.

Preserved
---------
- fix10 no-marker Reference retention
- pi_4^3 R1 (5.1)
- pi_4^3 R2 Proposition 5.1
- EHP exactness remains excluded from public Reference
- no target-group hard-code

Repository-wide pytest is not run.
