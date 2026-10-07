Phase 159-R1-6d

Purpose
-------
Finalize Toda (5.1) specialization derivation and Reference linkage in the
public Narrative.

Changes
-------
- Display the diagonal Toda (5.1) statement as pi_n^n = Z{iota_n}, using
  braces consistently with the rest of the project.
- Normalize Reference linkage prose to "[R1] より,".
- Explain the low-dimensional suspension isomorphism in the proof body:
  [R1] より, pi_1^1 = Z{iota_1}, pi_2^2 = Z{iota_2}.
  E(iota_1) = iota_2 であるから, E:pi_1^1 -> pi_2^2 は同型.
- Render the exact sequence as centered display math.
- Render numbered important map-property statements as centered display math.

Scope
-----
No low-dimensional fact or inference-rule logic is changed. This Phase
finalizes the public projection only and does not anticipate a later semantic
refactor.

Full pytest
-----------
Not run. Full-suite execution remains reserved for the end of Phase 159.
