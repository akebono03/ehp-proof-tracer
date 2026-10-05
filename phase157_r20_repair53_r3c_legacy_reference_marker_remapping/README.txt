Phase157-R20 repair53-r3c
legacy dedicated Reference marker remapping

Purpose
-------
The pi_15^8 dedicated renderer still writes the legacy body marker

  [R1] より, これらの生成元はそれぞれ

The current graph/fixed-boundary Reference entries are instead:

  R1 = Proposition 5.15
  R2 = Proposition 4.4

Therefore body-use filtering mistakes Proposition 5.15 for the used
Reference and drops Proposition 4.4.

Repair
------
Immediately before body-use filtering in
_phase153_r3_10_connect_public_reference_section(), only for pi_15^8:

1. Find the current Reference entry whose identity is
   locator == "Proposition 4.4".
2. Rewrite the legacy dedicated marker to that entry's current number.
3. Let the existing body-use filtering perform its normal filtering and
   final renumbering.

The patch does NOT hard-code "[R2]" as the final public marker.
It resolves Proposition 4.4 by Reference identity, so the pre-filter
number may change without breaking the mapping.

Files changed
-------------
Production:
  toda_group_proof_narrative_renderer.py

Test added:
  tests/test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py

No import changes.
No classification changes.
No fixed-statement boundary changes.
No graph-entry changes.
No repository-wide pytest.

Focused completion conditions
-----------------------------
- pi_15^8 retains Proposition 4.4 after body-use filtering.
- The final public Reference is numbered consistently.
- The dedicated body marker points to the retained Proposition 4.4.
- No stale [R2] marker remains after final filtering.
- Existing repair53-r3 focused tests are re-run when present.

Phase boundary
--------------
This repair only fixes legacy dedicated Reference marker remapping.
It does not generalize dedicated renderers or redesign Reference filtering.
Repository-wide pytest remains reserved for the end of Phase 157.
