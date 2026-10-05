Phase157-R20 repair39

Purpose
-------
Provide generic map-name fallback for concrete EHP map dataclasses whose
`.name` attribute is absent or None.

repair38 finding
----------------
The relevant map-property statements contain:

- TodaSuspensionMap, name=None
- TodaHopfInvariantMap, name=None

while the exactness window identifies the maps as:

- E
- H

Therefore repair37's map matching never succeeds.

Generic repair
--------------
Change:
- _toda_group_proof_narrative_map_name_latex()

Rules:
- explicit `.name` remains authoritative;
- if `.name is None`:
  - TodaSuspensionMap -> E
  - TodaIteratedSuspensionMap -> E
  - TodaHopfInvariantMap -> H
  - TodaDeltaMap -> \Delta
- unknown map types -> None

No group dimension, generator, proposition number, or pi_6^3-specific
condition is used.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

Changed function
----------------
- _toda_group_proof_narrative_map_name_latex()

Import changes
--------------
None.

New test
--------
- tests/test_phase157_r20_repair39_map_type_name_fallback.py

Completion condition
--------------------
- concrete map objects resolve to E/H/\Delta;
- repair37 short-exact ordering starts matching its support steps;
- short exact derivation appears after visible injectivity and surjectivity;
- Phase156 Reference regression remains passing.

No documentation changes.
No repository-wide pytest.
