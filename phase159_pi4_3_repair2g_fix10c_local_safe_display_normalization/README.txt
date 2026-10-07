Phase 159 repair2g fix10c

Purpose
-------
Retry fix10b with a local-state-safe insertion strategy.

The previous fix10b failed before changing production code because its
apply script assumed that
normalize_toda_group_proof_narrative_display_math_periods()
was present at a specific local insertion point.

fix10c does not depend on that helper.

Changed file
------------
toda_group_proof_narrative_contribution_renderer.py

New helper
----------
normalize_toda_group_proof_narrative_numbered_map_property_display()

Insertion position
------------------
Immediately before the existing function:

render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

Changed function
----------------
render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

The helper is called immediately before generic_used_step_ids is built.
This preserves the existing internal \\tag-based ordering and reference
logic and changes only the public display representation.

Normalization
-------------
- $<map>\\tag{N}$ は単射.
  ->
  \\[
  <map>\\quad\\text{は単射}. \\qquad (N)
  \\]

The same applies to 全射 and 同型.

- は零写像である.
  ->
  は零写像.

Preserved
---------
- fix10 Reference retention
- pi_4^3 R1 (5.1)
- pi_4^3 R2 Proposition 5.1
- EHP exactness remains excluded from public Reference
- no n/k-specific renderer hard-code

Repository-wide pytest is not run.
