Phase 159 R1-7c R4 exact-sequence subsequence suppression repair1

Scope
-----
Suppress only a redundant exact-sequence subsequence when the same proof
already displays a strictly longer exact sequence containing it.

Observed pi_3^2 issue
---------------------
The public Narrative displays:

  pi_2^1 -> pi_3^2 -> pi_3^3 -> pi_1^1 -> pi_2^2

and then repeats the contained fragment:

  pi_2^1 -> pi_3^2 -> pi_3^3 -> pi_1^1

The shorter sequence is redundant.

Production change
-----------------
File:
  toda_group_proof_narrative_contribution_renderer.py

Changed function:
  merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows

General rule:
- build the adjacent-window merged sequence as before;
- if its sequence core is already contained in a displayed sequence with
  strictly more arrows, remove the shorter exactness fragments and do not
  insert the merged subsequence again;
- otherwise retain the existing merge behavior.

No pi_3^2 special case is introduced.

Not changed
-----------
- eta_2 wording;
- theorem or semantic data;
- exactness graph;
- reference logic;
- equation numbering;
- Proposition 5.3 generator canonicalization.

Tests
-----
New:
  tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py

Existing focused regression:
  tests/test_phase157_r20_repair32_exactness_intro_anchor.py

Generator canonicalization regression:
  tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py

Full pytest is intentionally not run during Phase 159.
