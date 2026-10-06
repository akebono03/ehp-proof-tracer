Phase 159 repair2g fix10f

Purpose
-------
Move numbered map-property display normalization to the final public
equation-number normalization layer.

Why fix10e was insufficient
---------------------------
fix10e successfully normalized:
  は零写像である.
to:
  は零写像.

However the final public Narrative still showed:
  $H: ...\tag{1}$ は単射.

The final public renderer applies:
  _phase158_normalize_public_equation_numbers()
after the contribution-renderer stage.

Therefore equation-number formatting belongs in that final layer.

Changed files
-------------
1. toda_group_proof_narrative_renderer.py

Changed function:
  _phase158_normalize_public_equation_numbers()

After final equation-number retention/renumbering, numbered map-property
lines are rendered as:

  \[
  H: ...\quad\text{は単射}. \qquad (1)
  \]

The same applies to:
- 単射
- 全射
- 同型

Zero-map wording is also normalized there:
  は零写像である.
  ->
  は零写像.

2. toda_group_proof_narrative_contribution_renderer.py

The ineffective fix10e helper
  normalize_toda_group_proof_narrative_numbered_map_property_display()
and its call are removed.

Preserved
---------
- fix10 no-marker Reference retention
- pi_4^3 R1 (5.1)
- pi_4^3 R2 Proposition 5.1
- EHP exactness is not a public Reference
- no n/k-specific rendering branch

Tests
-----
- pi_3^2 Narrative contract
- repair2g focused tests
- repair1 / repair1c health checks

Repository-wide pytest is not run.
