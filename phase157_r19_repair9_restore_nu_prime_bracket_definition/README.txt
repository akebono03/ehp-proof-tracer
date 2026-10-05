Phase157-R19 repair9

Purpose
-------
Restore the defining Toda-bracket membership for nu' to the public
Reference entry [R2] (5.3), while continuing to hide the internal
Lemma 5.2 / bracket derivation machinery from the public proof body.

Public [R2] becomes:

  nu' in {eta_3, 2 iota_4, eta_4}_1  (define nu' this way)
  nu' in pi_6^3
  2 nu' = eta_3^3
  H(nu') = eta_5

Changed files
-------------
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py
- tests/test_phase157_r3_pi6_3_reference_boundary.py

No import changes.
No documentation changes.
No repository-wide pytest.
