Phase157-R19 repair6

Current state before this repair:
- R1 through R5 are all present.
- Proposition 2.2 / Proposition 5.3 support for Delta=0 is present and ordered.
- Remaining failures are only the old public calculation paragraphs:
  tag(1)-tag(3) and tag(4)-tag(6).

Repair6 changes only:
  _phase157_r19_finalize_pi6_3_public_narrative()

Instead of replacing one large exact multiline string, it canonicalizes
paragraphs by equation tags. This is robust against the renderer's later
period normalization.

Expected public changes:
- tag(1)-tag(3) collapse to:
    [R2]より, 2 nu' = eta_3^3.
- tag(4)-tag(6) collapse to:
    [R2]より, H(nu') = eta_5.
- pi_6^5 is explicitly attributed to [R4].
- after E injectivity, the nonzero reason
    E(eta_2^3)=eta_3^3 != 0
  is inserted before the existing order statement.

Files changed:
- toda_group_proof_narrative_contribution_renderer.py

No import changes.
No test changes.
No documentation changes.
No repository-wide pytest.
