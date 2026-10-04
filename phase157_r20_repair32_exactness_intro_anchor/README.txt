Phase157-R20 repair32

Purpose
-------
Place a merged four-term EHP exactness statement at the already-visible
introductory sequence position when that position exists.

Current failure
---------------
The public proof begins with a bare four-term EHP sequence immediately after:

  "次の完全列を考える."

But the merged statement saying that the same sequence is exact appears later,
after the Hopf-surjectivity support. This makes the proof-order contract fail.

Generic rule
------------
When two adjacent EHP exactness windows are merged:
1. build the merged four-term bare sequence;
2. search the current public paragraphs for exactly that bare sequence;
3. if it appears exactly once, use that paragraph as the merged exactness
   anchor;
4. remove the two component exactness paragraphs and the bare duplicate;
5. insert one merged "... は完全である." paragraph at the introduction anchor.

If no unique bare sequence is visible, retain the previous behavior and insert
at the earlier component-exactness position.

No group dimension, generator, proposition number, or pi_6^3-specific
condition is used.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

Changed function
----------------
- merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows()

New test
--------
- tests/test_phase157_r20_repair32_exactness_intro_anchor.py

Completion condition for this repair
------------------------------------
- the full exactness statement precedes the eta_6 suspension bridge;
- the bare duplicate four-term sequence is absent;
- existing Phase157 ordering/reference regressions continue to pass as far as
  the next independent defect.

No documentation changes.
No repository-wide pytest.
