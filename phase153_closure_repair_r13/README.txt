Phase 153 Closure Repair R13
=============================

Defects found by the 112-group closure audit
--------------------------------------------
1. pi_4^2:
   root (5.2) remained because LiteratureReference equality compared the full
   label + locator object instead of canonical locator identity.

2. pi_8^5:
   the specialized public Reference connector re-expanded all structural
   References, reintroducing Proposition 5.6 and two unused entries.

3. pi_15^8:
   the same specialized connector replaced the specialized external
   Proposition 4.4 Reference with the structural root Proposition 5.15.

General repair
--------------
- LiteratureReference identity is locator-first when both locators exist.
- The specialized public connector first filters structural entries by the
  markers actually used by the specialized proof body.
- Root Reference exclusion is then applied.
- If root exclusion would invalidate the specialized body's existing marker
  mapping, the connector preserves the specialized renderer's own Reference
  section rather than replacing it with a wrong public mapping.

Changed production files
------------------------
toda_group_proof_narrative_references.py
toda_group_proof_narrative_renderer.py

Added test
----------
tests/test_phase153_closure_repair_r13.py

Phase boundary
--------------
No proof prose cleanup is included.
Full pytest is not run here.
If the focused tests and 112-group audit pass, run the Phase 153 final full
pytest next.
