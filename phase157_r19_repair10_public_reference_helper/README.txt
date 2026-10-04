Phase157-R19 repair10

Cause
-----
repair9 correctly added the nu' Toda-bracket definition to the finalizer,
but the later helper
  _phase157_r19_public_reference_statement_lines()
overwrote the (5.3) public statements with three lines and removed it again.

Change
------
Only the later public-reference helper is changed.

[R2] (5.3) now contains:
- nu' in {eta_3, 2 iota_4, eta_4}_1 とする.
- nu' in pi_6^3.
- 2 nu' = eta_3^3.
- H(nu') = eta_5.

Internal Lemma 5.2 proof machinery remains hidden.

Changed file
------------
- toda_group_proof_narrative_contribution_renderer.py

No import changes.
No test changes.
No documentation changes.
No repository-wide pytest.
