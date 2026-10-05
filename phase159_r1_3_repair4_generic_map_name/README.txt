Phase 159-R1-3 repair4

Diagnosis confirmed:
- definition node exists
- isomorphism premise exists
- generic isomorphism check is True
- maps are equal
- TodaHopfInvariantMap.name is None

Fix:
Reuse the existing generic renderer helper `_generic_group_map_name()`.
That helper already maps TodaHopfInvariantMap -> H, TodaSuspensionMap -> E,
TodaDeltaMap -> \\Delta, etc.

Production changes:
- toda_group_proof_narrative_renderer.py
  - import `_generic_group_map_name`
  - replace `_phase159_unique_preimage_definition_line()`

Test changes:
none

Full pytest:
not run
