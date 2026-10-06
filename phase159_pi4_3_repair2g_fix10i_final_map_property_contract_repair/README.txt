Phase 159 repair2g fix10i

Purpose
-------
Repair the actual final Phase159-R4 map-property normalization layer.

fix10h confirmed that:
- _phase158_normalize_public_equation_numbers() receives no numbered
  map-property tags,
- the later Phase159-R4 map-property normalizer adds the tags,
- replacing the injective/surjective lines with sentinels prevents tags
  from appearing.

Changed file
------------
toda_group_proof_narrative_renderer.py

Changed functions
-----------------
1. _phase159_r1_7c_r4_normalize_public_map_property_prose()

Terse wording is now applied to the whole public Narrative, including
Reference content:
- は単射である. -> は単射.
- は全射である. -> は全射.
- は同型写像である. -> は同型.
- は同型である. -> は同型.
- は零写像である. -> は零写像.

2. _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning()

The existing semantic detection of matching injective/surjective/
isomorphism map properties is preserved.

Instead of inserting \tag{N} into inline math, the selected injective
and surjective facts are emitted as display math:

  \[
  H: ...\quad\text{は単射}. \qquad (1)
  \]

The isomorphism derivation remains:

  (1), (2) より, $H: ...$ は同型.

Preserved
---------
- Reference selection
- fix10 no-marker Reference retention
- pi_4^3 R1 (5.1)
- pi_4^3 R2 Proposition 5.1
- EHP exactness remains excluded from public Reference
- no n/k-specific rendering branch

Tests
-----
- pi_3^2 Narrative contract
- repair2g focused tests
- repair1 / repair1c health checks

Repository-wide pytest is not run.
