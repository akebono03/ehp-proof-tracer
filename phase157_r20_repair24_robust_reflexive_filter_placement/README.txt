Phase157-R20 repair24

Purpose
-------
Repair the repair23 application failure without relying on one exact local
string shape.

Cause
-----
repair23 assumed one exact accidental repair22 insertion block existed.
The user's cumulative local file did not match that exact text, so repair23
stopped before writing any production changes.

Robust strategy
---------------
1. Locate `render_toda_group_proof_narrative_argument_body_markdown()` by AST.
2. Within that function only, remove every existing invocation of
   `_is_toda_group_proof_narrative_rendered_reflexive_equality_step(proof_step)`.
3. Locate the unique `display_steps = tuple(...)` block.
4. Insert the helper call exactly once after the `context_hidden_step_ids`
   predicate inside that block.
5. Verify there is exactly one helper call in the whole body-renderer function.

The helper definition from repair22 is reused unchanged.

Changed production file
-----------------------
- toda_group_proof_narrative_argument_body_renderer.py

Changed function
----------------
- render_toda_group_proof_narrative_argument_body_markdown()

New test
--------
- tests/test_phase157_r20_repair24_robust_reflexive_filter_placement.py

No documentation changes.
No repository-wide pytest.
