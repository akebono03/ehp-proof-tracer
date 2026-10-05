Phase157-R20 repair53 — Display closing fragment normalization

Changed production file
-----------------------
- toda_group_proof_narrative_renderer.py

Changed / added units
---------------------
1. New function:
   _normalize_toda_group_proof_narrative_display_closing_fragments()
   Inserted immediately before:
   _finalize_toda_group_proof_narrative_markdown()

2. Changed function:
   _finalize_toda_group_proof_narrative_markdown()
   Adds one generic final-normalization call after connector/numeric
   normalization and before line-level section/QED handling.

3. New focused test:
   tests/test_phase157_r20_repair53_display_closing_fragment_normalization.py

Import changes
--------------
None.

General rule
------------
When a standalone closing prose fragment immediately follows a display-math
block with only blank lines in between, remove those blank lines so the closing
prose belongs to the same paragraph.

Handled fragments:
- である.
- を得る.
- を用いる.
- となる.

The text itself is not rewritten. Mathematical statements, proof graph,
references, ordering, and QED behavior are unchanged.

Expected effect
---------------
pi_8^5:
  the final "を得る." is no longer an isolated paragraph.

pi_15^8:
  the two "である." and two "を得る." fragments are no longer isolated
  paragraphs.

Out of scope for repair53
-------------------------
- pi_4^3 root statement repeated twice
- pi_4^3 eta_3 = eta_3 display

Those have different ownership and will be handled separately after repair53.

Focused pytest
--------------
- repair53 tests
- Phase134 pi_8^5 / pi_15^8 contracts
- recent repair42-48 focused regressions

Then re-run repair51 audit.

Repository-wide pytest remains deferred to Phase157 closure.
