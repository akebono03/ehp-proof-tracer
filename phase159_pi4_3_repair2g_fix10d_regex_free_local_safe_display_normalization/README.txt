Phase 159 repair2g fix10d

Purpose
-------
Retry fix10c with a regex-free apply script.

fix10c failed before changing production code because the helper used to
locate Python function spans contained an incorrectly escaped regular
expression.

fix10d removes regular expressions entirely.

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

Normalization call position
---------------------------
Immediately before generic_used_step_ids is built.

Generic public-display normalization
------------------------------------
- $<map>\tag{N}$ は単射.
  becomes display math with
  \quad\text{は単射}. \qquad (N)

The same applies to 全射 and 同型.

- は零写像である.
  becomes
  は零写像.

Preserved
---------
- fix10 no-marker Reference retention
- pi_4^3 R1 (5.1)
- pi_4^3 R2 Proposition 5.1
- EHP exactness remains absent from public Reference
- no target-group hard-code

Function-span algorithm
-----------------------
The apply script finds:

  def <function_name>(

and uses the next top-level:

  \ndef 

as the end boundary.

Repository-wide pytest is not run.
