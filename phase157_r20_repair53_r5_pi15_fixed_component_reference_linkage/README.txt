Phase157-R20 repair53-r5
pi_15^8 fixed-component Reference linkage

Finding from repair53-r4b
-------------------------
The exact proof body uses:

  pi_14^7 = Z/8{sigma'}

before applying Proposition 4.4.

The Phase157 literature boundary classifies that relation as:

  FIXED_STATEMENT
  reference_locator = Proposition 5.15
  component_key = pi14_7_group_relation

However, public Reference currently contains only Proposition 4.4.

A second mismatch also exists after root exclusion:

  remaining Proposition 5.15 proof step:
    pi_14^7 finite cyclic

  statement line:
    pi_15^8 decomposition

Repair
------
Only the pi_15^8 dedicated public Reference connection path is changed.

1. Resolve Proposition 5.15 by Reference identity.
2. Resolve its pi_14^7 proof step from the existing entry.
3. Replace the legacy "既に" introduction of that exact rendered
   pi_14^7 statement with the current Proposition 5.15 [R#] marker.
4. Continue to resolve Proposition 4.4 by Reference identity, as r3c did.
5. After root exclusion, regenerate statement lines from the filtered
   entries so the remaining pi_14^7 component renders its own statement.

Expected public result
----------------------
Reference:

  [R1] Proposition 5.15
  pi_14^7 = Z/8{sigma'}

  [R2] Proposition 4.4
  decomposition isomorphism

Proof:

  [R1] ... pi_14^7 = Z/8{sigma'}
  ...
  [R2] ... generator images

The Proposition 5.15 root component pi_15^8 is not repeated in
Reference.

Files
-----
Production:
  toda_group_proof_narrative_renderer.py

Updated focused test:
  tests/test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py

Imports
-------
No import changes.

Repository-wide pytest
----------------------
Not run. Reserved for the end of Phase 157.

Phase boundary
--------------
This repair is limited to the pi_15^8 dedicated Reference linkage and
post-root-exclusion statement-line refresh.

It does not generalize dedicated renderers, change literature-boundary
classification, alter Reference identity, or change unrelated groups.
