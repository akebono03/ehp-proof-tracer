Phase 159 repair2g fix10b

Purpose
-------
Complete the generic public-display contract already expected by the
current Phase159 pi_3^2 tests.

Observed mismatch
-----------------
Current public output:
- numbered map properties use inline \\tag{1}, \\tag{2},
- zero-map wording still says "は零写像である.".

Current Phase159 contract expects:
- display-math numbered map properties:
  H: ... \\quad\\text{は単射}. \\qquad (1)
- terse zero-map wording:
  "は零写像."

Changed file
------------
toda_group_proof_narrative_contribution_renderer.py

New function
------------
normalize_toda_group_proof_narrative_numbered_map_property_display()

Insertion position
------------------
Immediately before:
normalize_toda_group_proof_narrative_display_math_periods()

Changed function
----------------
render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

Change
------
Call the new normalization function immediately before
build_toda_group_proof_narrative_generic_used_step_ids().

Why this position
-----------------
All semantic dependency ordering, reference-linking, equation-reference
reasoning, and \\tag-based internal processing have already completed.
Only the final public-display representation changes.

Generic behavior
----------------
A paragraph of the form:

  $<map latex>\\tag{N}$ は単射.

becomes:

  \\[
  <map latex>\\quad\\text{は単射}. \\qquad (N)
  \\]

The same normalization applies to:
- 単射
- 全射
- 同型

Additionally:
- "は零写像である." becomes "は零写像."

No pi_3^2 or pi_4^3 target hard-code is added.

Preserved
---------
- fix10 no-marker Reference retention
- pi_4^3 R1 (5.1)
- pi_4^3 R2 Proposition 5.1
- EHP exactness remains absent from public Reference
- repair1 direct Proposition 5.1 Delta provenance

Tests
-----
- current pi_3^2 Narrative contract
- repair2g focused tests
- repair1 / repair1c health checks

Repository-wide pytest is not run.
