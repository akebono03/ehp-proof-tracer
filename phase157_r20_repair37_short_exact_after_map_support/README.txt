Phase157-R20 repair37

Purpose
-------
Order each generated short exact sequence after the visible injectivity and
surjectivity statements that justify it.

Current defect
--------------
The generic proof-block renderer generates a short exact sequence when the
matching injective and surjective steps exist in the presentation, but it does
not require those map-property statements to appear earlier in the public
Narrative.

Therefore the body can say:

  "left map is injective and right map is surjective, hence short exact"

before the right-map surjectivity has actually been shown.

Generic repair
--------------
Add:
- order_toda_group_proof_narrative_short_exact_support()

For each exactness step that produces a generic short exact sequence:
1. identify the exactness window;
2. find the matching visible injective map statement;
3. find the matching visible surjective map statement;
4. find the short-exact reason paragraph and sequence paragraph;
5. move the reason + sequence after the later of the two map-property
   paragraphs.

No group dimension, generator, proposition number, or pi_6^3-specific
condition is used.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

Import changes
--------------
The generic narrative renderer import block additionally imports:
- _generic_short_exact_sequence_latex
- _generic_short_exact_sequence_reason_prose

New function
------------
- order_toda_group_proof_narrative_short_exact_support()

Insertion point
---------------
Immediately after:
- order_toda_group_proof_narrative_surjectivity_support()

Pipeline change
---------------
Run short-exact support ordering immediately after surjectivity support
ordering.

New test
--------
- tests/test_phase157_r20_repair37_short_exact_after_map_support.py

Completion condition
--------------------
- injectivity < surjectivity support chain < surjectivity < short-exact reason
  < short-exact sequence;
- existing Phase157 dependency-ordering tests continue to pass until the next
  independent defect;
- Phase156 Reference regressions remain passing.

No documentation changes.
No repository-wide pytest.
